import pygame as pg
pg.init()
from GUI_elements import*
import clr
import traceback
from random import randint
import sys, os

gray1 = pg.Color(33, 33, 33)
gray2 = pg.Color(67, 67, 67)

class Dino():
    def __init__(self, img_dark = None, img_light = None, size = (147, 150), pos = (50, 450)):
        self.img_dark = img_dark
        self.img_light = img_light
        self.rect = pg.Rect(pos, size)
        self.pos = list(pos)
        self.v = 0
        self.locked = False
    def show(self, screen, screenCol):
        if screenCol == clr.black:
            image = self.img_dark
        else:
            image = self.img_light
        screen.blit(image, self.pos)
    def move(self, a = -2.2):
        if self.locked:
        	a = -2.2
        self.v -= a
        self.pos[1] += int(self.v)
        if self.pos[1] > 450:
            self.pos[1] = 450
            self.v = 0
            self.locked = False
        elif self.pos[1] < 450:
            self.locked = True
        self.rect[1] = self.pos[1]


class Bush():
    def __init__(self, img_list_light, img_list_dark, pos, speed = 20):
        self.pos = list(pos)
        self.img_list_light = img_list_light	
        self.img_list_dark = img_list_dark
        self.image_d = None
        self.image_l = None
        self.rect = pg.Rect(pos, (0,0))
        self.speed = speed
    def show(self, screen, screenCol):
        if self.image_d == None or self.pos[0] < -150:
            if self.image_d != None:
                rand = randint(-1, 1)
                self.pos[0] = 2150 + rand*50
            rand = randint(0,2)
            if rand == 1:
            	self.pos[1] = 427
            else:
            	self.pos[1] = 475
            self.image_d = self.img_list_dark[rand]
            self.image_l = self.img_list_light[rand]
        if screenCol == clr.black:
        	image = self.image_d
        	col = gray2
        else:
        	image = self.image_l
        	col = gray1
        self.rect[2], self.rect[3] = image.get_rect()[2], image.get_rect()[3]
        screen.blit(image, self.pos)
    def move(self):
        self.pos[0] -= self.speed
        self.rect[0] = self.pos[0]
    def crash(self, dino):
        temp = self.rect.colliderect(dino.rect)
        return temp

def mainLoop(screenCol, textCol):
    screenWd, screenHt = 1120, 630
    screen = pg.display.set_mode((screenWd, screenHt))
    screenCenter = (screenWd//2, screenHt//2)
    clock = pg.time.Clock()
    count = 0
    score = 0
    FPS = 20
    alive = True
    center = (screenWd //2, 100)
    paused = False

    img_light_small = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_s_light.png"))
    img_light_large = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_d_light.png"))
    img_light_double = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_l_light.png"))
    img_light_dino = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_light.png"))

    img_dark_small = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_s.png"))
    img_dark_large = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_d.png"))
    img_dark_double = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_l.png"))
    img_dark_dino = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino.png"))

    dino = Dino(img_dark_dino, img_light_dino)

    bush1 = Bush([img_light_small, img_light_double, img_light_large], [img_dark_small, img_dark_double ,img_dark_large], (900, 475))
    bush2 = Bush([img_light_small, img_light_double, img_light_large], [img_dark_small, img_dark_double ,img_dark_large], (1700, 475))
    bush3 = Bush([img_light_small, img_light_double, img_light_large], [img_dark_small, img_dark_double ,img_dark_large], (2500, 475))

    butt_mode = Button(1075, 15, 20, 20)

    bush_list = [bush1, bush2, bush3]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit()
                if event.key == pg.K_SPACE:
                    if paused:
                        paused = False
                    else:
                        dino.move(30)
                elif event.key == pg.K_p and alive:
                    if paused:
                        paused = False
                    else:
                    	text(screen, 0, 0, 50, "Paused", textCol, center)
                    	paused = True

        if butt_mode.get_click():
            if screenCol == clr.black:
                screenCol = clr.white
                textCol = clr.black
            else:
                screenCol = clr.black
                textCol = clr.white

        screen.fill(screenCol)

        for bush in bush_list:
            if alive and paused == False:
                bush.move()
            bush.show(screen, screenCol)
            if bush.crash(dino):
                alive = False
                new, home, origin = lose(screen, screenCenter, score)
            if score % 20 == 0:
                bush.speed += 0.1

        if alive == False:
            new, home, origin = lose(screen, screenCenter, score)
            if home.get_click(origin):
                return False, screenCol, textCol
            if new.get_click(origin):
                return True, screenCol, textCol

        dino.show(screen, screenCol)

        if count%(FPS//4) == 0 and alive and paused == False:
                score += 1

        text(screen, screenWd - 100, 5, 30, str(score), textCol)
        
        if alive and paused == False:
        	dino.move()

        if screenCol == clr.black:
        	col = gray2
        	sun(screen)
        else:
        	col = gray1
        	moon(screen)

        if paused:
            text(screen, 0, 0, 50, "Paused", textCol, center)
        else:
            count += 1

        pg.draw.line(screen, col, (0, 585), (1120, 585), 4)
        pg.display.update()
        clock.tick(FPS)



# try:
#     restart, screenCol, textCol = mainLoop(clr.white, clr.black)
#     while restart:
#         restart, screenCol, textCol = mainLoop(screenCol, textCol)
# except:
#     traceback.print_exc()
# finally:
#     Quit()