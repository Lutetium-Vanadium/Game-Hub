import pygame as pg
pg.init()
import math
import clr


class Button():
    def __init__(self, x, y, wd, ht, text = '', img = None, hovourImg = None, textHeight = None, textColour = clr.black,
                 colour = clr.gray, hovourColour = clr.light_gray, opaque = True, activated = True, outline = False,
                 hovour = True, value = None, surfpos = (0,0), enabled_selected = True, isSize = False):
        if not textHeight:
            textHeight = ht//5
        self.textHeight = textHeight
        self.img = img
        self.hovourImg = hovourImg
        self.xy = (x, y)
        self.surfpos = surfpos
        self.rect = pg.Rect(x, y, wd, ht)
        self.text = text
        self.textColour = textColour
        self.colour = colour
        self.hovourColour = hovourColour
        self.hovour = hovour
        self.opaque = opaque
        self.activated = activated
        self.flag = False
        self.outline = outline
        self.value = value
        self.enabled_selected = enabled_selected
        self.selected = False
        self.isSize = isSize
    def onButton(self, origin = None):
        if origin == None:
            origin = self.surfpos
        mpos = list(pg.mouse.get_pos())
        mpos[0] -= origin[0]
        mpos[1] -= origin[1]
        return self.rect.collidepoint(mpos)
    def show(self, surface, origin = None, canvas = None):
        if origin == None:
            origin = self.surfpos
        if self.onButton(origin) and self.hovour:
            if self.img:
                image = self.hovourImg
            else:
                colour = self.hovourColour
        else:
            if self.img:
                image = self.img
            else:
                colour = self.colour
        if self.img:
            surface.blit(image, self.xy)
        elif self.opaque:
            pg.draw.rect(surface, colour, self.rect)
        if self.enabled_selected and self.selected:
            thickness = 3
            col = clr.select_green
        else:
            thickness = 1
            col = self.textColour
        if self.isSize:
            pg.draw.line(surface, clr.black, (450, 50), (550, 50))
        if self.outline:
            pg.draw.line(surface, col, self.rect.topleft, self.rect.topright, thickness)
            pg.draw.line(surface, col, self.rect.bottomright, self.rect.topright, thickness)
            pg.draw.line(surface, col, self.rect.bottomleft, self.rect.bottomright, thickness)
            pg.draw.line(surface, col, self.rect.bottomleft, self.rect.topleft, thickness)
        textSurf = pg.font.SysFont(pg.font.get_default_font(), self.textHeight).render(self.text, True, self.textColour)
        textRect = textSurf.get_rect()
        textRect.center = self.rect.center
        surface.blit(textSurf, textRect)
    def get_click(self, origin = None):
        if origin == None:
            origin = self.surfpos
        temp = (self.activated and pg.mouse.get_pressed()[0] and self.onButton(origin))
        if self.flag == False and temp:
            self.flag = True
            return temp
        if self.flag and temp == False:
            self.flag = False

class Text():
    def __init__(self, x, y,  size, surfsize, text = '', colour = pg.Color("BLACK")):
        self.location = [x, y]
        self.size = size
        self.text = text
        self.colour = colour
        self.surf = pg.Surface(surfsize)
        self.rect = self.surf.get_rect()
    def display(self, screen):
        textSurf = pg.font.SysFont(pg.font.get_default_font(), self.size).render(self.text, True, self.colour)
        textRect = textSurf.get_rect()
        textRect.center = self.rect.center
        screen.blit(textSurf, self.location)
'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
def Quit():
    pg.quit()
    exit()

def text(screen, x , y, size, text, colour = clr.white, center = None):
    textSurf = pg.font.SysFont(pg.font.get_default_font(), size).render(text, True, colour)
    if center:
        textRect = textSurf.get_rect()
        textRect.center = center
        x, y = textRect.topleft
    screen.blit(textSurf, (x, y))

def lose(screen, screenCenter, score):
    surf = pg.Surface((400, 200))
    surf.fill(clr.light_light_gray)
    surfRect = surf.get_rect()
    surfRect.center = screenCenter
    text(surf, 0, 0, 30, ("Your Score is: "+str(score)), clr.black, (200, 30))
    text(surf, 0, 0, 30, "Crashed!", clr.black, (200, 70))
    new = Button(30, 125, 140, 50, 'new game', textHeight = 30, outline = True)
    home = Button(230, 125, 140, 50, 'home', textHeight = 30, outline = True)
    new.show(surf, surfRect.topleft)
    home.show(surf, surfRect.topleft)
    pg.draw.line(surf, clr.black,(0,0), (0,200))
    pg.draw.line(surf, clr.black, (0,199), (399,199))
    pg.draw.line(surf, clr.black, (399,199), (399,0))
    pg.draw.line(surf, clr.black, (400,0), (0,0))

    screen.blit(surf, surfRect.topleft)
    return new, home, surfRect.topleft

def sun(screen):
    surf = pg.Surface((200, 200))
    surf.fill(clr.black)
    surf.set_colorkey(clr.black)
    pg.draw.circle(surf, clr.white, (100, 100), 70)
    for i in range(12):
        start_x = 50 * (math.cos(i*math.pi/6))
        end_x = 100 * (math.cos(i*math.pi/6))
        start_y = 50 * (math.sin(i*math.pi/6))
        end_y = 100 * (math.sin(i*math.pi/6))
        pg.draw.line(surf, clr.white, ((100 + start_x),(100 + start_y)), ((100 + end_x),(100 + end_y)), 30)
    surf = pg.transform.smoothscale(surf, (20, 20))
    screen.blit(surf, (1075, 15))

def moon(screen):
    surf = pg.Surface((200, 200))
    surf.fill(screen.get_at((1085, 25)))
    pg.draw.circle(surf, clr.black, (100, 100), 100)
    pg.draw.circle(surf, screen.get_at((1085, 25)), (180, 100), 100)
    surf = pg.transform.smoothscale(surf, (20, 20))
    c = surf.get_at((0,0))
    surf.set_colorkey(c)
    screen.blit(surf, (1075, 15))
