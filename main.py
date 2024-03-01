# BUG: scrolling counts as click(maybe check if left click), changing any settings requierreas you to reset board (otherwise very wierd things happen)((not really a bug)), max recursion depth error
# BUG: if mines low you can instantly win, changing width/height if different size will make the window VERY small, the executable is VERY BUGGY (infinite sound, cant save files)
# TODO: make counters for mines left and time, make own images(wont happen lol), make better music (wont happen lol)
# TODO: maybe make the mines sound not loop -_- idk
# TODO: make restart button resize, add about page or more, background image = the border like minesweeper (scales with size), nicer settings, build the app to exe
# TODO: config file(all values stored in json?) ... and some fun .... .stu...fff....

# Guide on how to build (for myself):
# use resourcePath function in vars everywhere
# in .spec file in datas include all files that are used I only use the data folder so it is this: datas=[('data/*','data')]
# run pyinstaller -> a lot of errors -> 3 hours of debugging -> profit
try:
    import gameSettings
    
    import vars
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
    import pygame.freetype
except ImportError as err:
    print ("couldn't load module. %s" % (err))
    sys.exit(2)

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')





#not used and i dont know if it works...
def GridToWorld(x,y):
    return (x*vars.var.CELL_SIZE* (vars.var.currentSize+1),y*vars.var.CELL_SIZE* (vars.var.currentSize+1))


#handles all scenes
class GameState():
    def __init__(self):
        self.state = "main_game"
        vars.var = vars.Variables()
        # Loads from file
        vars.var.saveLoad("load")
        
        self.sansText = 0
        self.sansOpen = 0
        self.sansTalk = None
        self.sansCanLeave = False
    #trigger every frame always
    def always(self):
        return

    # THE ACTUAL GAME VERY IMPORTANT
    def mainGame(self):
                
        events = pygame.event.get()
        for event in events:
            #end while
            if event.type == QUIT:
                vars.var.run = False
            #f1 = reset
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    restartBoard()
                if event.key == K_ESCAPE:
                    self.state = "settings"
                #not a good time
                if event.key == K_s:
                    self.sansOpen += 1
                    self.state = "sans"
                    sound = pygame.mixer.Sound(vars.var.resourcePath("data/sans_talk.mp3"))
                    sound.set_volume(0.7)
                    sound.play(-1)
                    self.sansTalk = sound
                    music.stop()
                    restartBoard()
                    vars.var.NUMOFMINES = int((vars.var.GRID_WIDTH * vars.var.GRID_HEIGHT) /3)
                # change visual size of board
                if event.key == K_F2:
                    #infinitely bigger just for fun
                    vars.var.currentSize += 1
                    resizeBoard(vars.var.currentSize)
                if event.key == K_1:
                    resizeBoard(0)
                if event.key == K_2:
                    resizeBoard(1)
                if event.key == K_3:
                    resizeBoard(2)

                # HOWT O SDO RESIZNI NG IGEHLPEHLEPHLEPHLEplHPELHPHELEPHLEPHLEHLp
            elif event.type == VIDEORESIZE:
                #restartButton.surf = pygame.transform.scale(restartButton.surf, event.dict['size'])
                pygame.display.update()
            elif event.type == VIDEOEXPOSE:  # handles window minimising/maximising
                vars.var.screen.fill((0, 0, 0))
                #restartButton.surf = pygame.transform.scale(restartButton.surf, screen.get_size())
                pygame.display.update()

        # End game (reveal everything, play boom sound, change face) should probably be moved to a function
        if vars.var.endGame:
            vars.var.restartButton.changeFace(4)
            boom.play()
            for field in vars.var.grid:
                field.covered = False
                field.image = field.getSquareImage()

        checkWin()

        # render
        vars.var.screen.blit(vars.var.background, (0, 0))

        for entity in vars.var.grid:
            vars.var.screen.blit(entity.surf, entity.rect,vars.var.multiplyTuple(entity.image,vars.var.currentSize+1))
        for entity in vars.var.other_sprites:
            vars.var.screen.blit(entity.surf, entity.rect,entity.image)
        
        NUMBERSFONT = pygame.freetype.SysFont("Arial",10)
        #displays leftover mines
        vars.var.DrawText(NUMBERSFONT,(10,10),str(vars.var.minesLeft))
        # update
        vars.var.other_sprites.update(events)
        vars.var.grid.update(events)

        pygame.display.flip()

    #this is an [[REDACTED]]
    def sans(self):
        events = pygame.event.get()
        for event in events:
            #end while
            if event.type == QUIT:
                vars.var.run = False
            if event.type == KEYDOWN:
                if event.key == K_s or event.key == K_RETURN:
                    if self.sansCanLeave:
                        self.sansCanLeave = False
                        self.sansText = 0
                        changeMusic(vars.var.resourcePath("data/megalovania.mp3"))
                        self.state = "main_game"
                if event.key == K_F1:
                    vars.var.mail = True
                    playSound(vars.var.resourcePath("data/youve-got-mail-sound.mp3"),loop=-1)
        
        FONT = SANS_FONT

        text = "you're gonna have a bad time."
        if self.sansOpen > 3:
            text = "A VERY VERY BAD TIME"
        if self.sansOpen > 5:
            FONT = G_FONT
            text = "A " + "VERY "*(self.sansOpen-5) + "BAD TIME"

        #characters dont appear at once (yes it is tied to framerate currently 20 so not good but also this entire screen is just a meme so no one cares i dont even know if somebody will read this)
        if self.sansText < len(text):
            self.sansText += 1
        else:
            self.sansCanLeave = True
            self.sansTalk.stop()
        # render
        vars.var.screen.blit(vars.var.background, (0, 0))
        vars.var.DrawText(FONT,(0,0),text[:self.sansText])
        pygame.display.flip()

    #actual settings in different file
    def settings(self):
        gameSettings.settingsMain()
        return

    #Calls function according to the self.state
    def stateManager(self):
        self.always()
        if self.state == "main_game":
            self.mainGame()
        elif self.state == "about":
            self.about()
        elif self.state == "settings":
            self.settings()
        elif self.state == "sans":
            self.sans()

# Class for the tiles in game
class Square(pygame.sprite.Sprite):
    

    def __init__(self):
        super(Square,self).__init__()
        # vars.var
        self.number = 0
        self.covered = True #covered(1)/uncovered(0)
        self.isMine =  False    #mine(1)/no mine(0)
        self.flagged = False
        self.clicked = False
        self.position = (0,0)
        self.image = self.getSquareImage()

        # Loading img
        self.surf = pygame.image.load(vars.var.getSpritesheetLocation()).convert()
        
        self.small_surf = self.surf
        self.surf = pygame.transform.scale(self.surf,(139*(vars.var.currentSize+1),84*(vars.var.currentSize+1)))
        #self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(width = 16,height = 16)

    #returns current image (position on spritesheet)
    def getSquareImage(self):
        if self.covered:
            if self.flagged:
                img = vars.var.FLAG
            else:
                img = vars.var.NOT_CLICKED
        elif self.isMine:
            if self.clicked:
                img = vars.var.RED_MINE
            else:
                img = vars.var.MINE
        else:
            img = self.getNumberInSquare()
        return img

    #sub function, gets position in spritesheets according to number
    def getNumberInSquare(self):
        if self.number == 0:
            num = vars.var.EMPTY
        else:
            num = vars.var.NUMBERS[self.number - 1]
        return num

    #updates hitbox, used when changing size of board
    def updateSize(self):
        self.rect.width = vars.var.CELL_SIZE* (vars.var.currentSize+1)
        self.rect.height = vars.var.CELL_SIZE* (vars.var.currentSize+1)
    #called every frame, handles clicking
    def update(self, events):

        for event in events:
            #CLICK
            if event.type == MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.click()
                    elif event.button == 3:
                        self.rightClick()

    #left click, reveal or lose game
    def click(self,checkFlags = True):
        # ensures safe first click (rerolls board unil the click isnt a mine)
        if vars.var.firstClick:
            while self.isMine or self.number != 0:
                deleteMines()
                distributeMines()
                makeNumbers()
            vars.var.firstClick = False
        
        if self.covered and not self.flagged:#uncover if not uncovered already or doesnt have flag    also clicked and update the image
            if self.isMine:
                vars.var.endGame = True
            self.covered = False
            self.clicked = True
            self.image = self.getSquareImage()
        elif not self.covered and not self.flagged and checkFlags and self.number != 0:
            self.destroyAdjacent()
        
        if not self.flagged and self.number == 0:
            try:
                self.recursiveDestroy()
            except:
                print("MAX RECURSION ERROR")
    
    #right click(wow), handles flags
    def rightClick(self):
        if self.covered:
            #toggles flag and updates mines left
            if self.flagged:
                self.flagged = False
                vars.var.minesLeft += 1
            else:
                self.flagged = True
                vars.var.minesLeft -= 1
            #updates image
            self.image = self.getSquareImage()

    def destroyAdjacent(self):
        gridArray = vars.var.grid.sprites()

        x = self.position[0]
        y = self.position[1]
        adjacentLocations = getAdjacentArrayLocations(x,y)
        num = 0
        # count number of flags
        for adjField in adjacentLocations:
            if adjField != "NULL" and gridArray[adjField].flagged:
                num += 1
        
        # same number as flags -> destroy(click) everything else
        if self.number == num:
            for adjField in adjacentLocations:
                if adjField != "NULL":
                    gridArray[adjField].click(checkFlags=False)
        
    #called from click calls click on adjacent tiles if empty
    def recursiveDestroy(self):

        gridArray = vars.var.grid.sprites()

        x = self.position[0]
        y = self.position[1]
        adjacentLocations = getAdjacentArrayLocations(x,y)

        # clickAdjacent
        for adjField in adjacentLocations:
            if adjField != "NULL" and gridArray[adjField].covered:
                gridArray[adjField].click(checkFlags=False)

    #returns true if at least 1 adjacent tile is covered /can be optimized/ 
    def hasAdjacent(self):
        hasAdjecent = False
        gridArray = vars.var.grid.sprites()
        x = self.position[0]
        y = self.position[1]
        if gridArray[getIndexInGrid(x+1,y)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x-1,y)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x,y+1)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x,y-1)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x+1,y+1)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x-1,y-1)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x+1,y-1)].covered:
            hasAdjecent = True
        if gridArray[getIndexInGrid(x-1,y+1)].covered:
            hasAdjecent = True
        return hasAdjecent

    # Not used but works
    def updateImg(self):
        self.image = self.getSquareImage()
    
    def debugPrint(self):
        print(self.covered)
        print(self.isMine)
        print(self.flagged)
        print(self.clicked)

#the button at the top, resets the board
class RestartButton(pygame.sprite.Sprite):
    def __init__(self):
        super(RestartButton,self).__init__()
        # vars.var
        self.image = vars.var.FACES[0]
        # Loading img
        self.surf = pygame.image.load(vars.var.getSpritesheetLocation()).convert()
        #self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(width = 25,height = 25, center = (vars.var.SCREEN_WIDTH/2,25/2))

    #call every frame, clicking -> restartBoard(), updating image
    def update(self,events):
        for event in events:
            #clicking "animation"
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.changeFace(1)
                    #fun
                    if vars.var.mail:
                        playSound(vars.var.resourcePath("data/youve-got-mail-sound.mp3"))
            #actual clicking
            if event.type == MOUSEBUTTONUP:
                self.changeFace(0)
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        restartBoard()
            #nurthing
            if event.type == VIDEORESIZE:
                print("nurthing")
        self.rect = self.surf.get_rect(width = 25,height = 25, center = (vars.var.screen.get_width()/2,25/2))
        # Epic gamer moment veri funnnnnnnnnnnnni
        keys = pygame.key.get_pressed()
        if (keys[K_6] and keys[K_9]) or (keys[K_4] and keys[K_2] and keys[K_0]):
            self.changeFace(3)
    def changeFace(self,face):
        self.image = vars.var.FACES[face]

def getIndexInGrid(x,y):
    if 0 > x or x >= vars.var.GRID_WIDTH or 0 > y or y >= vars.var.GRID_HEIGHT:
        return "NULL"
    return (x*vars.var.GRID_HEIGHT + y)

def getAdjacentArrayLocations(x,y):
    right = getIndexInGrid(x+1,y)
    left = getIndexInGrid(x-1,y)
    up = getIndexInGrid(x,y+1)
    down = getIndexInGrid(x,y-1)
    upRight = getIndexInGrid(x+1,y+1)
    downLeft = getIndexInGrid(x-1,y-1)
    downRight = getIndexInGrid(x+1,y-1)
    upLeft = getIndexInGrid(x-1,y+1)
    return [right,left,up,down,upRight,downLeft,downRight,upLeft]

def checkWin():
    # Check if everything except mines is revealed
    win = True
    for field in vars.var.grid:
        if not field.isMine and field.covered:
            win = False
            break
    
    # Call win function
    if win and not vars.var.endGame:
        vars.var.other_sprites.sprites()[0].changeFace(3)
        for field in vars.var.grid:
                if field.isMine and not field.flagged:
                    field.flagged = True
                    field.image = field.getSquareImage()

def changeMusic(path):
    global music
    music.stop()
    music = pygame.mixer.Sound(path)
    music.play(-1)

def playSound(path,volume=1,loop = 0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play(loop)

def resizeBoard(num):
    vars.var.currentSize = num
    restartBoard()

    vars.var.screen = pygame.display.set_mode((vars.var.SCREEN_WIDTH*(vars.var.currentSize+1),vars.var.SCREEN_HEIGHT*(vars.var.currentSize+1)))


    vars.var.background = pygame.Surface(vars.var.screen.get_size())
    vars.var.background = vars.var.background.convert()
    vars.var.background.fill((192, 192, 192))
        
def deleteMines():
    for field in vars.var.grid:
        field.isMine = False

def buildGrid():
    # Init grid
    for row in range(vars.var.GRID_WIDTH):
        for col in range(vars.var.GRID_HEIGHT):
            sq = Square()
            sq.rect.center = (row*vars.var.CELL_SIZE* (vars.var.currentSize+1)+vars.var.GRID_START[0],col*vars.var.CELL_SIZE* (vars.var.currentSize+1)+vars.var.GRID_START[1])
            sq.position = (row,col)
            vars.var.grid.add(sq)

def distributeMines():
        # Distributes mines
    mineCounter = 0
    while mineCounter < vars.var.NUMOFMINES:
        mine = random.choice(vars.var.grid.sprites())
        if not mine.isMine:
            mine.isMine = True
            mineCounter += 1

def makeNumbers():
    gridArray = vars.var.grid.sprites()
    for field in vars.var.grid:
        x = field.position[0]
        y = field.position[1]
        adjacentLocations = getAdjacentArrayLocations(x,y)
        num = 0
        for adjField in adjacentLocations:
            if adjField != "NULL" and gridArray[adjField].isMine:
                num += 1
        field.number = num

def restartBoard():
    vars.var.endGame = False
    vars.var.firstClick = True
    vars.var.grid.empty()
    buildGrid()
    distributeMines()
    makeNumbers()
    for field in vars.var.grid:
        field.updateSize()
    vars.var.minesLeft = vars.var.NUMOFMINES

#   MAIN
vars.var.gameState = GameState()
# Initialise screen
pygame.init()
vars.var.screen = pygame.display.set_mode((vars.var.SCREEN_WIDTH,vars.var.SCREEN_HEIGHT))
pygame.display.set_caption('MINESWEEPER')

# Change icon to mine
programIcon = pygame.image.load(vars.var.resourcePath('data/mine.jpg'))
pygame.display.set_icon(programIcon)
# Fill background
vars.var.background = pygame.Surface(vars.var.screen.get_size())
vars.var.background = vars.var.background.convert()
vars.var.background.fill((192, 192, 192))

# Fonts
ARIAL_FONT = pygame.freetype.SysFont('Arial', 10)
SANS_FONT = pygame.freetype.SysFont('Comic Sans MS', 20)
G_FONT = pygame.freetype.SysFont('papyrus', 30,bold=True)
# Groups

vars.var.grid = pygame.sprite.Group()

vars.var.other_sprites = pygame.sprite.Group()

# Other buttons
vars.var.restartButton = RestartButton()
vars.var.other_sprites.add(vars.var.restartButton)

# Prepare board

buildGrid()

distributeMines()

makeNumbers()

resizeBoard(vars.var.currentSize)
pygame.mixer.init()
# Sounds
mail_sound = pygame.mixer.Sound(vars.var.resourcePath("data/youve-got-mail-sound.mp3"))
music = pygame.mixer.Sound(vars.var.resourcePath("data/mine music.wav"))
boom = pygame.mixer.Sound(vars.var.resourcePath("data/boom.wav"))
# hehe jumpscare
boom.set_volume(0.3)
music.set_volume(0.4)
music.play(-1,)

# Init other scripts
gameSettings.init()

# Custom events
#MAKESQUARE = pygame.USEREVENT + 1
#pygame.time.set_timer(MAKESQUARE, 1000)

vars.var.gameState.state = "main_game"
clock = pygame.time.Clock()
# Event loop
vars.var.run = True
while vars.var.run:
    vars.var.gameState.stateManager()
    # 20 fps
    clock.tick(20)


pygame.quit()


