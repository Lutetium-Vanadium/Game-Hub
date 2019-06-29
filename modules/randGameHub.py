import pygame as pg
pg.init()
import random as rand
from GUI_elements import*
import clr

butt_mode = Button(1075, 15, 20, 20)

#####################################################################################################################################################################################################3

class RandCircle():
    def __init__(self, r = 10, x = 560, y = 315):
        self.circ = [x, y]
        self.colour = clr.red
        self.r = r
    def move(self, surfHt, surfWd, speed):
        rand1 = rand.randint(-speed,speed)
        rand2 = rand.randint(-speed,speed)
        self.circ[0] += rand1                                                                       ## Generating 
        self.circ[1] += rand2                                                                       ## random ints
        if self.circ[0]+self.r < 0 or self.circ[0]-self.r > surfWd:
            self.circ[0] -= rand1
        if self.circ[1]+self.r < 0 or self.circ[1]-self.r > surfHt:
            self.circ[1] -= rand2
    def show(self, surface):
        pg.draw.circle(surface, self.colour, (self.circ[0], self.circ[1]), self.r)                  ## Drawing circle

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

def difficultyChoice(screenCol, textCol):
    Bool = True
    FPS = 25
    screenWidth, screenHeight = (1120, 630)
    screen = pg.display.set_mode((screenWidth, screenHeight))
    clock = pg.time.Clock()

    buttE = Button(360, 36, 400, 142, "Easy", colour = clr.green, hovourColour = clr.light_green)
    buttM1 = Button(110, 214, 350, 142, "Medium 1", colour = clr.orange, hovourColour = clr.light_orange)
    buttM2 = Button(570, 214, 350, 142, "Medium 2", colour = clr.orange, hovourColour = clr.light_orange)
    buttH = Button(360, 392, 400, 142, "Hard", colour = clr.red, hovourColour = clr.light_red)
    butt_exit = Button(1050, 600, 50, 30, "Exit", textHeight = 30, textColour = textCol, opaque = False)
    butt_mainMenu = Button(940, 600, 100, 30, "Main Menu", textHeight = 30, textColour = textCol, opaque = False)

    while Bool:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit()

        if buttE.get_click():
            speed = 6
            size = 10
            Bool = False
        elif buttM1.get_click():
            speed = 12
            size = 10
            Bool =False
        elif buttM2.get_click():
            speed = 6
            size = 5
            Bool = False
        elif buttH.get_click():
            speed = 12
            size = 5
            Bool = False
        elif butt_exit.get_click():
            Quit()
        elif butt_mode.get_click():
            if screenCol == clr.black:
                screenCol = clr.white
                textCol = clr.black
            else:
                screenCol = clr.black
                textCol = clr.white
            butt_mainMenu.textColour = butt_exit.textColour = textCol
        elif butt_mainMenu.get_click():
            return screenCol, textCol, False, None

        screen.fill(screenCol)
        
        if screenCol == clr.black:
            sun(screen)
        else:
            moon(screen)

        if buttE.onButton():
            text(screen, 30, 585, 30, "Easy: Slow speed, Big circle.", textCol)
        elif buttM1.onButton():
            text(screen, 30, 585, 30, "Medium 1: Fast speed, Big circle.", textCol)
        elif buttM2.onButton():
            text(screen, 30, 585, 30, "Medium 2: Slow speed, Small circle.", textCol)
        elif buttH.onButton():
            text(screen, 30, 585, 30, "Hard: Fast speed, Small circle.", textCol)

        buttE.show(screen)
        buttM1.show(screen)
        buttM2.show(screen)
        buttH.show(screen)
        butt_exit.show(screen)
        butt_mainMenu.show(screen)
        pg.display.update()

        clock.tick(FPS)

    return screenCol, textCol, speed, size

def mainLoop(screenCol, textCol, speed, size):
    FPS = 25
    screenWidth, screenHeight = (1120, 630)
    screen = pg.display.set_mode((screenWidth, screenHeight))
    clock = pg.time.Clock()
    
    circle = RandCircle(size)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if screen.get_at(pg.mouse.get_pos()) == clr.red:
                    text(screen, 310, 285, 79, "Congrats! Clicked!", textCol)
                    pg.display.update()
                    pg.time.wait(2500)
                    return screenCol, textCol

        if butt_mode.get_click():
            if screenCol == clr.black:
                screenCol = clr.white
                textCol = clr.black
            else:
                screenCol = clr.black
                textCol = clr.white

        screen.fill(screenCol)
        
        if screenCol == clr.black:
            sun(screen)
        else:
            moon(screen)
        
        circle.move(screenWidth, screenHeight, speed)
        
        circle.show(screen)
        pg.display.update()
        
        clock.tick(FPS)

##########################################################################################################################################################################

#speed, size = difficultyChoice()
#mainLoop(speed, size)
