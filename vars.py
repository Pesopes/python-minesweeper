import pickle
import os
import sys


class Variables:
    def __init__(self):
        
        self.endGame = False
        self.grid = None
        self.other_sprites = None
        self.firstClick = True
        self.currentSize = 1
        self.gameState = None
        self.screen = None
        self.background = None
        self.restartButton = None
        self.run = True
        self.game = None
        self.minesLeft = 10
        #fun stuff
        self.mail = False

        #SPRITESHEET LOCATIONS
        self.NOT_CLICKED = (0,51,16,16)
        self.EMPTY = (17,51,16,16)
        self.FLAG = (34,51,16,16)
        self.MINE = (85,51,16,16)
        self.RED_MINE = (102,51,16,16)
        self.FACES = [(0,24,25,25),(27,24,25,25),(54,24,25,25),(81,24,25,25),(108,24,25,25)]
        self.NUMBERS = [(0,68,16,16),(17,68,16,16),(34,68,16,16),(51,68,16,16),(68,68,16,16),(85,68,16,16),(102,68,16,16),(119,68,16,16)]
        self.DIGITS = [(126,0,12,22),(0,0,12,22),(14,0,12,22),(28,0,12,22),(42,0,12,22),(56,0,12,22),(70,0,12,22),(84,0,12,22),(98,0,12,22),(112,0,12,22)]



        # CONSTS
        self.SPRITESHEETS = ["data/minesweeper_sprites.png","data/minesweeper_sprites_spook.jpg","data/minesweeper_sprites_kid.jpg","data/minesweeper_sprites_random.png"]
        self.CURRENTSPRITESHEET = 0
        self.BACKGROUND_COLOR = (192,192,192)
        # Mines in grid
        self.NUMOFMINES = 10
        self.GRID_START = (16,35)
        self.GRID_WIDTH = 9
        self.GRID_HEIGHT = 9
        self.CELL_SIZE = 16
        self.SCREEN_WIDTH = self.GRID_WIDTH*self.CELL_SIZE * self.currentSize+self.GRID_START[0]
        self.SCREEN_HEIGHT = self.GRID_HEIGHT*self.CELL_SIZE* self.currentSize+self.GRID_START[1]

    # Functions

    def multiplyTuple(self,tuple, amount):
        out = ()
        for num in tuple:
            out += (num * amount,)
        return out


    #add better positional functionality (like aligning)
    def DrawText(self,font,pos,text,rgb=(0,0,0)):
        font.render_to(self.screen, pos, text, rgb)

    #just does the same thing as when it starts
    def updateScreenDimensions(self):
        self.SCREEN_WIDTH = self.GRID_WIDTH*self.CELL_SIZE * self.currentSize+self.GRID_START[0]
        self.SCREEN_HEIGHT = self.GRID_HEIGHT*self.CELL_SIZE* self.currentSize+self.GRID_START[1]

    def getSpritesheetLocation(self):
        i = self.CURRENTSPRITESHEET
        return var.resourcePath(self.SPRITESHEETS[i])

    #for pyinstaller
    def resourcePath(self,relative_path):
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    #saves only some variables
    def saveLoad(self,opt):
        filename = self.resourcePath("data/var.pkl")
        if opt == "save":

            f = open(filename, 'wb')
            pickle.dump([self.NUMOFMINES,self.GRID_WIDTH,self.GRID_HEIGHT], f, 2)
            f.close

            print ('data saved')
        elif opt == "load":
            f = open(filename, 'rb')
            self.NUMOFMINES,self.GRID_WIDTH,self.GRID_HEIGHT = pickle.load(f)
            self.updateScreenDimensions()
        else:
            print ('Invalid saveLoad option')

# Globals
var = Variables()