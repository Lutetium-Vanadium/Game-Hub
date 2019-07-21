import pygame as pg
pg.init()
from GUI_elements import*
import clr, traceback
from random import randint
import sys, os

################################################################################################################################################################################################

class Pipe():
    def __init__(self, x, y, flip, ht , wd = 100, speed = 3, topHt = 40, botWd = None,
                 col = clr.green, high_col = clr.light_green, shad_col = clr.dark_green):
        self.surf = pg.Surface((wd, ht))
        self.size = [wd, ht]
        self.coord = [x, y]
        self.topHt = topHt
        self.top_rect = pg.Rect(0, 0, wd, topHt)
        if botWd == None:
            botWd = 4*wd//5
        self.botWd = botWd
        self.bot_rect = pg.Rect((wd - botWd)//2, topHt, botWd, (ht - topHt))
        self.colScheme = [high_col, col, shad_col]
        self.flip = flip                                                  # True for top and False for bottom
        self.speed = speed
    def show(self, screen, screenHt, i, pipe_list, block):
        if self.coord[0] < (-self.size[0]):
            if self.flip:
                self.size[1] = randint(1, block-1) * screenHt//block
            else:
                self.size[1] = screenHt - (pipe_list[i%(len(pipe_list)//2)].size[1] + screenHt//block)
            self.coord[0] = 1400

        
        self.surf.fill(clr.sky)
        
        pg.draw.rect(self.surf, self.colScheme[1], self.top_rect)
        pg.draw.rect(self.surf, self.colScheme[0], (self.top_rect.topleft, (self.size[0]//5, self.topHt)))
        pg.draw.rect(self.surf, self.colScheme[2], ((4 * self.size[0]//5, 0), (self.size[0]//5, self.topHt)))
        pg.draw.rect(self.surf, self.colScheme[1], self.bot_rect)
        pg.draw.rect(self.surf, self.colScheme[0], (self.bot_rect.topleft, (self.botWd//5, self.bot_rect[3])))
        pg.draw.rect(self.surf, self.colScheme[2], (((4 * self.botWd//5) + self.bot_rect.left, self.bot_rect.top), (self.botWd//5, self.bot_rect[3])))
        
        pg.draw.line(self.surf, clr.black, self.top_rect.topleft, self.top_rect.topright, 5)
        pg.draw.line(self.surf, clr.black, self.top_rect.bottomright, self.top_rect.topright, 5)
        pg.draw.line(self.surf, clr.black, self.top_rect.bottomleft, self.top_rect.bottomright, 5)
        pg.draw.line(self.surf, clr.black, self.top_rect.bottomleft, self.top_rect.topleft, 5)
        
        pg.draw.line(self.surf, clr.black, self.bot_rect.topleft, self.bot_rect.topright, 5)
        pg.draw.line(self.surf, clr.black, self.bot_rect.bottomright, self.bot_rect.topright, 5)
        pg.draw.line(self.surf, clr.black, self.bot_rect.bottomleft, self.bot_rect.topleft, 5)

        self.surf.set_colorkey(clr.sky)

        
        self.surf = pg.transform.flip(self.surf, False, self.flip)
        
        screen.blit(self.surf, self.coord)
    def move(self):
        self.coord[0] -= self.speed
    def crash(self, bird):
        surfRect = self.surf.get_rect()
        surfRect[0] = self.coord[0]
        surfRect[1] = self.coord[1]
        return (surfRect.colliderect(bird.rect))

class Bird():
    def __init__(self, x, y, pic_up, pic_down):
        self.initpos = (x,y)
        self.pos = [x, y]
        self.pic_up = pic_up
        self.pic_down = pic_down
        self.speed = 0
        self.rect = (self.pos, (40, 40))
        self.v = 0
    def show(self, screen):
        if self.v > 0:
            screen.blit(self.pic_down, self.pos)
        else:
            screen.blit(self.pic_up, self.pos)
    def is_dead(self, screenHt):
        return self.pos[1] > screenHt
    def move(self, t, a = 2 ):
        self.v += a
        if self.v > 15:
            self.v = 15
        elif self.v < -25:
            self.v = -25
        
        self.pos[1] += self.v
        

################################################################################################################################################################################################
def cloud(screen, x, y, r=20):
    pg.draw.circle(screen, clr.white, (x, (y - r)), r)
    pg.draw.circle(screen, clr.white, (x + (r + 8), y), r)
    pg.draw.circle(screen, clr.white, ((x + int(2.5*r)), (y + r)), r)
    pg.draw.circle(screen, clr.white, ((x - r), (y + r//2)), r)
    pg.draw.circle(screen, clr.white, ((x+5), (y+5)), r)
    pg.draw.circle(screen, clr.white, ((x+r), (y+r)), r)
    pg.draw.rect(screen, clr.sky, (x-3*r, y+r, 8*r, r))    

def day_sky(screen):
    screen.fill(clr.sky)
    cloud(screen, 220, 150)
    cloud(screen, 947, 324)
    cloud(screen, 670, 500)
    
def mainLoop(screencol, textcol):
    pg.display.set_caption('Flappy Bird')
    
    screenWd, screenHt = 1120, 630
    screenCenter = (screenWd//2, screenHt//2)
    screen = pg.display.set_mode((screenWd, screenHt))
    clock = pg.time.Clock()
    FPS = 25
    alive = True
    score = 0
    count = 0
    temp = 0
    block = 3
    paused = False
    center = (screenWd //2, 100)
    star_pos = [(randint(0, screenWd), randint(0, screenHt)) for i in range(10)]

    randintlist = [(randint(1, block-1) * screenHt//block) for i in range(5)]
    randintlist[0] = block//2 *screenHt//block
    
    pic_up = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "bird_up.png"))
    pic_down = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "bird_down.png"))

    top_pipe1 = Pipe(500, 0, True, randintlist[0])
    bot_pipe1 = Pipe(500, (randintlist[0] + screenHt//block), False, (screenHt - (randintlist[0] + screenHt//block)))
    top_pipe2 = Pipe(800, 0, True, randintlist[1])
    bot_pipe2 = Pipe(800, (randintlist[1] + screenHt//block), False, (screenHt - (randintlist[1] + screenHt//block)))
    top_pipe3 = Pipe(1100, 0, True, randintlist[2])
    bot_pipe3 = Pipe(1100, (randintlist[2] + screenHt//block), False, (screenHt - (randintlist[2] + screenHt//block)))
    top_pipe4 = Pipe(1400, 0, True, randintlist[3])
    bot_pipe4 = Pipe(1400, (randintlist[3] + screenHt//block), False, (screenHt - (randintlist[3] + screenHt//block)))
    top_pipe5 = Pipe(1700, 0, True, randintlist[4])
    bot_pipe5 = Pipe(1700, (randintlist[4] + screenHt//block), False, (screenHt - (randintlist[4] + screenHt//block)))

    butt_mode = Button(1075, 15, 20, 20)

    bird = Bird(50, 200, pic_up, pic_down)

    pipe_list = [top_pipe1, top_pipe2, top_pipe3, top_pipe4, top_pipe5,
                 bot_pipe1, bot_pipe2, bot_pipe3, bot_pipe4, bot_pipe5]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit()
                if event.key == pg.K_SPACE and alive:
                    if paused:
                        paused = False
                    else:
                        bird.move(count, -25)
                elif event.key == pg.K_p and alive:
                    if paused:
                        paused = False
                    else:
                        paused = True
                        text(screen, 0, 0, 50, "Paused", textcol, center)

        if butt_mode.get_click():
            if screencol == clr.black:
                screencol = clr.white
                textcol = clr.black
            else:
                screencol = clr.black
                textcol = clr.white

        if screencol == clr.black:
            screen.fill(screencol)
            for star in star_pos:
                pg.draw.circle(screen, clr.white, star, 3)
        else:
            screen.fill(clr.sky)
            day_sky(screen)

        if paused:
            text(screen, 0, 0, 50, "Paused", textcol, center)
        else:
            if alive:
                if bird.is_dead(screenHt):
                    alive = False
                bird.move(count)

        for i in range(len(pipe_list)):
            if alive and paused == False:
                pipe_list[i].move()
            pipe_list[i].show(screen, screenHt, i, pipe_list, block)
            if pipe_list[i].crash(bird):
                alive = False
                new, home, origin = lose(screen, screenCenter, score)

        if screencol == clr.black:
            sun(screen)
        else:
            moon(screen)

        if alive == False:
            new, home, origin = lose(screen, screenCenter, score)
            if home.get_click(origin):
                return False, screencol, textcol
            if new.get_click(origin):
                return True, screencol, textcol
                
        if paused == False:        
            count += 1
        if count % 25 == 0 and alive and paused == False:
            score += 1

        text(screen, screenWd - 70, 5, 30, str(score), textcol)

        bird.show(screen)

        pg.display.update()
        clock.tick(FPS)

##try:
##    restart = mainLoop()
##    while restart:
##        restart = mainLoop()
##except:
##    traceback.print_exc()
##finally:
##    pg.quit()
