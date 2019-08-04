import pygame as pg
pg.init()
from GUI_elements import*
import clr
import traceback
from random import randint
import sys, os
from help import*


class Dino():
    def __init__(self, img_dark_list, img_light_list, pos = (50, 450)):
        size = (img_dark_list[0].get_rect()[2], img_dark_list[0].get_rect()[3])
        self.img_dark_list = img_dark_list
        self.img_light_list = img_light_list
        self.rect = pg.Rect(pos, size)
        self.pos = list(pos)
        self.v = 0
        self.locked = False
        self.surf = pg.Surface((size))
        self.surf.blit(img_light_list[0], (0,0))
        self.surf.set_colorkey(clr.green_screen)
        self.mask = pg.mask.from_surface(self.surf)
        self.image_count = 0
    def show(self, screen, screenCol, count, alive, paused):
        if count % 2 == 0 and paused == False:
            self.image_count += 1
            self.image_count %= 2
        if screenCol == clr.black:
            image_list = self.img_dark_list

        else:
            image_list = self.img_light_list
        if alive:
            image = image_list[self.image_count]
        else:
            image = image_list[2]
        if self.locked:
            image = image_list[0]
        self.surf.fill(clr.green_screen)
        self.surf.blit(image, (0,0))
        self.surf.set_colorkey(clr.green_screen)
        self.mask = pg.mask.from_surface(self.surf)
        screen.blit(self.surf, self.pos)
    def move(self, a = -17):
        if self.locked:
        	a = -17
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
    def __init__(self, img_list_light, img_list_dark, pos, speed = 25):
        self.pos = list(pos)
        self.img_list_light = img_list_light
        self.img_list_dark = img_list_dark
        self.image_d = None
        self.image_l = None
        self.rect = pg.Rect(pos, (0,0))
        self.speed = speed
        self.mask = None
    def show(self, screen, screenCol):
        if self.image_d == None or self.pos[0] < -150:
            if self.image_d != None:
                rand = randint(-1, 1)
                self.pos[0] = 3200 + rand*50
            rand = randint(0,2)
            if rand == 1:
            	self.pos[1] = 440
            else:
            	self.pos[1] = 490
            self.image_d = self.img_list_dark[rand]
            self.image_l = self.img_list_light[rand]
        if screenCol == clr.black:
        	image = self.image_d
        	col = clr.dark_gray
        else:
        	image = self.image_l
        	col = clr.dark_dark_gray
        size = (image.get_rect()[2], image.get_rect()[3])
        surf = pg.Surface(size)
        surf.blit(image, (0,0))
        surf.set_colorkey(clr.green_screen)
        self.mask = pg.mask.from_surface(surf)
        self.rect[2], self.rect[3] = size
        screen.blit(surf, self.pos)
    def move(self):
        self.pos[0] -= self.speed
        self.rect[0] = self.pos[0]
    def crash(self, dino):
        offset_x = dino.rect[0] - self.rect[0]
        offset_y = dino.rect[1] - self.rect[1]
        overlap = self.mask.overlap(dino.mask, (offset_x, offset_y))
        return overlap

def mainLoop(screenCol, textCol, prev_screen = None, rect_pos = None):
    pg.display.set_caption("Dino Run")
    start = True
    screenWd, screenHt = 1120, 630
    screen = pg.display.set_mode((screenWd, screenHt))
    screenCenter = (screenWd//2, screenHt//2)
    clock = pg.time.Clock()
    count = -1
    score = 0
    FPS = 20
    alive = True
    center = (screenWd //2, 100)
    paused = False
    play = False

    img_light_small = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_s_light.png"))
    img_light_large = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_d_light.png"))
    img_light_double = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_l_light.png"))
    img_light_dino = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_light.png"))
    img_light_dino2 = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino2_light.png"))
    img_light_dead_dino = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_dead_light.png"))

    img_dark_small = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_s.png"))
    img_dark_large = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_d.png"))
    img_dark_double = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "img_l.png"))
    img_dark_dino = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino.png"))
    img_dark_dino2 = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino2.png"))
    img_dark_dead_dino = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_dead.png"))

    dino = Dino([img_dark_dino, img_dark_dino2, img_dark_dead_dino], [img_light_dino, img_light_dino2, img_light_dead_dino])

    bush1 = Bush([img_light_small, img_light_double, img_light_large], [img_dark_small, img_dark_double ,img_dark_large], (900, 475))
    bush2 = Bush([img_light_small, img_light_double, img_light_large], [img_dark_small, img_dark_double ,img_dark_large], (2000, 475))
    bush3 = Bush([img_light_small, img_light_double, img_light_large], [img_dark_small, img_dark_double ,img_dark_large], (3100, 475))

    butt_mode = Button(1075, 15, 20, 20)

    bush_list = [bush1, bush2, bush3]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fade(screen, True, col = screenCol)
                    return False, screenCol, textCol
                if event.key == pg.K_SPACE and alive:
                    if paused:
                        paused = False
                    elif play == False:
                        play = True
                    elif alive:
                        dino.move(95)
                elif event.key == pg.K_p and alive:
                    if paused:
                        paused = False
                    else:
                    	paused = True
                elif event.key == pg.K_h:
                    if play:
                        paused = True
                    fade(screen, True, col = screenCol)
                    help_screen(DINO_RUN, screenCol, textCol)
                elif event.key == pg.K_m:
                    if screenCol == clr.black:
                        screenCol = clr.white
                        textCol = clr.black
                    else:
                        screenCol = clr.black
                        textCol = clr.white
                elif event.key == pg.K_n:
                    return True, screenCol, textCol

        if butt_mode.get_click():
            if screenCol == clr.black:
                screenCol = clr.white
                textCol = clr.black
            else:
                screenCol = clr.black
                textCol = clr.white

        screen.fill(screenCol)

        if screenCol == clr.black:
            col = clr.gray
            sun(screen)
        else:
            col = clr.dark_gray
            moon(screen)

        pg.draw.line(screen, col, (0, 555), (1120, 555), 4)

        for bush in bush_list:
            if alive and paused == False and play:
                bush.move()
            bush.show(screen, screenCol)
            if bush.crash(dino):
                alive = False
                new, home, origin = lose(screen, screenCenter, score)
            if score % 100 == 0:
                bush.speed += 1

        if alive == False:
            new, home, origin = lose(screen, screenCenter, score)
            if home.get_click(origin):
                fade(screen, True, col = screenCol)
                return False, screenCol, textCol
            if new.get_click(origin):
                return True, screenCol, textCol

        dino.show(screen, screenCol, count, alive, paused)

        if count%(FPS//4) == 0 and alive and paused == False and play:
                score += 1

        text(screen, screenWd - 100, 5, 30, str(score), textCol)

        if alive and paused == False and play:
        	dino.move()
        if paused:
            text(screen, 0, 0, 50, "Paused", textCol, center)
        elif play:
            count += 1

        if play == False:
            text(screen, 0, 0, 50, "Press space to start", textCol, (560, 250))
        if start and prev_screen != None:
            expand(screen, screen.copy(), [rect_pos[0]-90, rect_pos[1]+90, 200, 113], prev_screen)
            start = False
        else:
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
