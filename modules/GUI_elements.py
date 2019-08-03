import pygame as pg
pg.init()
import math
import clr
from animations import*

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
            pg.draw.line(surface, clr.black, (450, 50), (550, 50), canvas.thick)
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
        return False

class Text():
    def __init__(self, x, y,  size, surfsize, text = '', colour = pg.Color("BLACK"), cursor = False, center = False):
        self.location = [x, y]
        self.size = size
        self.text = text
        self.textColour = colour
        self.surf = pg.Surface(surfsize)
        self.rect = self.surf.get_rect()
        self.cursor = cursor
        self.count = 0
        self.cursor_on = False
        self.surfsize = surfsize
        self.center = center
    def display(self, screen, FPS = 25):
        textSurf = pg.font.SysFont(pg.font.get_default_font(), self.size).render(self.text, True, self.textColour)
        textRect = textSurf.get_rect()
        textRect.center = self.rect.center
        self.surf.set_colorkey(clr.green_screen)
        self.surf.fill(clr.green_screen)
        if self.center:
            self.surf.blit(textSurf, textRect.topleft)
            if self.cursor:
                if self.count % (FPS//2) == 0:
                    if self.cursor_on:
                        self.cursor_on = False
                    else:
                        self.cursor_on = True
                self.count += 1
                if self.cursor_on:
                    
                    start_pos = list(textRect.topright)
                    start_pos[0] += 3
                    start_pos[1] -= 3
                    
                    end_pos = list(textRect.bottomright)
                    end_pos[0] += 3
                    end_pos[1] += 3
                    
                    pg.draw.line(self.surf, self.textColour, start_pos, end_pos, 2)
            surf = self.surf
        else:
            surf = textSurf
        screen.blit(surf, self.location)
'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
def Quit(screen):
    fade(screen, True, 0.5)
    pg.quit()
    exit()

def text(screen, x , y, size, text, colour = clr.white, center = None):
    textSurf = pg.font.SysFont(pg.font.get_default_font(), size).render(text, True, colour)
    if center:
        textRect = textSurf.get_rect()
        textRect.center = center
        x, y = textRect.topleft
    screen.blit(textSurf, (x, y))

def lose(screen, screenCenter, score, txt = 'Crashed!'):
    surf = pg.Surface((400, 200))
    surf.fill(clr.light_light_gray)
    surfRect = surf.get_rect()
    surfRect.center = screenCenter
    text(surf, 0, 0, 30, ("Your Score is: "+str(score)), clr.black, (200, 30))
    text(surf, 0, 0, 30, txt, clr.black, (200, 70))
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

def sun(screen, colour = clr.white, scale = (20, 20), pos = (1075, 15), r1 = 140, r2 = 200):
    surf = pg.Surface((400, 400))
    surf.fill(clr.black)
    surf.set_colorkey(clr.black)
    pg.draw.circle(surf, colour, (200, 200), r1)
    for i in range(12):
        start_x = r1//2 * (math.cos(i*math.pi/6))
        end_x = r2 * (math.cos(i*math.pi/6))
        start_y = r1//2 * (math.sin(i*math.pi/6))
        end_y = r2 * (math.sin(i*math.pi/6))
        pg.draw.line(surf, colour, ((200 + start_x),(200 + start_y)), ((200 + end_x),(200 + end_y)), 60)
    surf = pg.transform.smoothscale(surf, scale)
    screen.blit(surf, pos)

def moon(screen):
    surf = pg.Surface((200, 200))
    surf.fill(screen.get_at((1085, 25)))
    pg.draw.circle(surf, clr.black, (100, 100), 100)
    pg.draw.circle(surf, screen.get_at((1085, 25)), (180, 100), 100)
    surf = pg.transform.smoothscale(surf, (20, 20))
    c = surf.get_at((0,0))
    surf.set_colorkey(c)
    screen.blit(surf, (1075, 15))