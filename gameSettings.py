
try:
    import vars

    import sys
    import pygame
    from socket import *
    from pygame.locals import *
    import pygame.freetype
except ImportError as err:
    print ("couldn't load module. %s" % (err))
    sys.exit(2)

NUMBEROFCOUNTERS = 4
counters = pygame.sprite.Group()
presetButtons = pygame.sprite.Group()
selected = -1
NAME_FONT = None
CONFIRM_FONT = None

class Counter(pygame.sprite.Sprite):
    def __init__(self):
        super(Counter,self).__init__()

        self.number = 0
        self.position = 0
        self.name = "NAME"
        self.description = "It does stuff..."
        self.width = 12
        self.height = 22
        self.x = 0
        self.y = 0
        self.selected = False

        self.surf = pygame.image.load(vars.var.getSpritesheetLocation()).convert()
        self.rect = self.surf.get_rect(width = 12,height = 22)
    def update(self,events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and event.button == 1:
                    global selected
                    selected = self.position
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.changeNumber(1)
                if event.key == K_DOWN:
                    self.changeNumber(-1)
            elif event.type == MOUSEWHEEL:
               self.changeNumber(event.y)
    def changeNumber(self,num):
        if selected == self.position and self.isInBounds(self.number+num):
            self.number += num
    
    def asignStartingValues(self):
        if self.position == 0:
            self.number = vars.var.NUMOFMINES
            self.name = "Number of mines"
        elif self.position == 1:
             self.number = vars.var.GRID_WIDTH
             self.name = "Width"
        elif self.position == 2:
             self.number = vars.var.GRID_HEIGHT
             self.name = "Height"
        elif self.position == 3:
            self.number = vars.var.CURRENTSPRITESHEET + 1
            self.name = "Theme"

    def changeSettings(self):
        if self.position == 0:
            if self.isInBounds(self.number):
                vars.var.NUMOFMINES = self.number
        elif self.position == 1:
            if self.isInBounds(self.number):
                vars.var.GRID_WIDTH = self.number
        elif self.position == 2:
            if self.isInBounds(self.number):
                vars.var.GRID_HEIGHT = self.number
        elif self.position == 3:
            if self.isInBounds(self.number):
                vars.var.CURRENTSPRITESHEET = self.number - 1 

        resizeScreen()

    def getImageAtIndex(self,i):
        numString = str(self.number)
        num = int(numString[i])
        image = vars.var.DIGITS[num]
        return image

    def isInBounds(self, num):
        if self.position == 0:
            if 0 < num < (vars.var.GRID_WIDTH * vars.var.GRID_HEIGHT):
                return True
        elif self.position == 1:
            if 0 < num <= 60:
                return True
        elif self.position == 2:
            if 0 < num <= 30:
                return True
        elif self.position == 3:
            if 0 < num < len(vars.var.SPRITESHEETS)+1:
                return True
        return False

class Button(pygame.sprite.Sprite):
    def __init__(self):
        super(Button,self).__init__()

        self.name = "NAME"
        self.description = "It does stuff..."
        self.func = None

        self.surf = pygame.image.load(vars.var.getSpritesheetLocation()).convert()
        self.rect = self.surf.get_rect(width = 16,height = 16)
    def update(self,events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and event.button == 1:
                    print("I "+ self.name +" have been clicked")
                    self.func()


def init():
    global NAME_FONT
    global CONFIRM_FONT
    NAME_FONT = pygame.freetype.SysFont('Arialblack', 15)
    CONFIRM_FONT = pygame.freetype.SysFont('Arial', 10)
    #cant use size on freetype fonts so i make an exact copy using normal pygame fonts smh my head
    CHEAP_FONT = pygame.font.SysFont("Arialblack",15)
    lastPos = 0
    #Counters
    for num in range(NUMBEROFCOUNTERS):
        c = Counter()
        c.position = num
        c.asignStartingValues()
        c.rect.center = (pygame.font.Font.size(CHEAP_FONT,c.name)[0]+15,num*22+22)
        counters.add(c)
        if num == NUMBEROFCOUNTERS-1:
            lastPos = num*22+22
            print(lastPos)
    #preset buttons
    NAMES = ["EASY","MEDIUM","HARD"]
    FUNCTIONS = [setEasy, setMedium, setHard]
    for num in range(3):
        b = Button()
        b.name = NAMES[num]
        b.func = FUNCTIONS[num]
        b.rect.center = (10,lastPos+32+(num * 24))
        presetButtons.add(b)


def leave():
    global selected
    selected = -1
    vars.var.gameState.state = "main_game"
def resizeScreen():
    vars.var.updateScreenDimensions()
    vars.var.screen = pygame.display.set_mode((vars.var.SCREEN_WIDTH*(vars.var.currentSize+1),vars.var.SCREEN_HEIGHT*(vars.var.currentSize+1)),RESIZABLE)

    vars.var.background = pygame.Surface(vars.var.screen.get_size())
    vars.var.background = vars.var.background.convert()
    vars.var.background.fill(vars.var.BACKGROUND_COLOR)

def settingsMain():
    #event handling
    events = pygame.event.get()
    
    for event in events:
        #end while
        if event.type == QUIT:
            vars.var.run = False
        if event.type == KEYDOWN:
            global selected
            if event.key == K_RIGHT:
                selected += 1
            if event.key == K_LEFT:
                selected -= 1
            if event.key == K_ESCAPE:
                leave()

            if event.key == K_RETURN:
                enterSettings()
            #saving
            if event.key == K_F12:
                vars.var.saveLoad("save")
            #loading
            if event.key == K_F11:
                vars.var.saveLoad("load")
                for entity in counters:
                    entity.asignStartingValues()

    # render
    vars.var.screen.blit(vars.var.background, (0, 0))

    for entity in counters:
        #pygame.draw.rect(vars.var.screen,(50*entity.position,100,10),entity.rect)

        if entity.position == selected and entity.selected == False:
            entity.surf.fill((0, 105, 0, 100), special_flags=pygame.BLEND_ADD)
            entity.selected = True
        elif entity.position != selected and entity.selected == True:
            entity.surf = pygame.image.load(vars.var.getSpritesheetLocation()).convert()
            entity.selected = False
        #draw numbers
        for i in range(len(str(entity.number))):
            x = entity.rect.centerx+(entity.rect.w*i)
            y = entity.rect.centery
            vars.var.screen.blit(entity.surf, (x-(entity.rect.width/2),y-(entity.rect.height/2)),entity.getImageAtIndex(i))
        #draw name of settings
        vars.var.DrawText(NAME_FONT,(1,entity.rect.centery),entity.name,(0,0,0))

    for entity in presetButtons:
        vars.var.screen.blit(entity.surf, entity.rect , vars.var.FACES[2])
    vars.var.DrawText(CONFIRM_FONT,(10,presetButtons.sprites()[-1].rect.bottomright[1]+20),"PRESS ENTER TO CONFIRM",(10,100,10))
    # update
    counters.update(events)
    presetButtons.update(events)

    pygame.display.flip()

def enterSettings():
    print("CONFIRMED SETTINGS")
    for entity in counters:
        entity.changeSettings()
    vars.var.minesLeft = vars.var.NUMOFMINES

def setEasy():
    c = counters.sprites()
    c[0].number = 10 #mines
    c[1].number = 9 #width
    c[2].number = 9 #height

def setMedium():
    c = counters.sprites()
    c[0].number = 40 #mines
    c[1].number = 16 #width
    c[2].number = 16 #height

def setHard():
    c = counters.sprites()
    c[0].number = 99 #mines
    c[1].number = 30 #width
    c[2].number = 16 #height