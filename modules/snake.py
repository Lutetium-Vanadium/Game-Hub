import pygame as pg
pg.init()
from GUI_elements import *
from help import *
import traceback
from random import randint

# CONSTANTS
HEIGHT = 60
WIDTH = 112
TOP_OFFSET = 12
BLOCKSIZE = 10

MOVES = {
    pg.K_UP: ([0, -1], [0, 1]),
    pg.K_DOWN: ([0, 1], [0, -1]),
    pg.K_RIGHT: ([1, 0], [-1, 0]),
    pg.K_LEFT: ([-1, 0], [1, 0])
}

class Snake():
    def __init__(self, start_length=4, velocity=[1, 0]):
        self.snake = self.initSnake(start_length)
        self.velocity = velocity

    def show(self, screen, colour):
        for block in self.snake:
            pg.draw.rect(screen, colour, (((block[0] * BLOCKSIZE), ((block[1] * BLOCKSIZE) + TOP_OFFSET)), (BLOCKSIZE, BLOCKSIZE)))

    def move(self):
        headX, headY = self.snake[0]
        new_snake = [((headX + self.velocity[0])%WIDTH, (headY + self.velocity[1])%HEIGHT)]
        for i in range(len(self.snake) - 1):
            new_snake.append(self.snake[i])

        self.snake = new_snake

    def get_rect(self, pos):
        return pg.Rect(pos[0] * BLOCKSIZE, pos[1] * BLOCKSIZE + TOP_OFFSET, BLOCKSIZE, BLOCKSIZE)

    def collide(self, apple):
        eaten = False
        selfRect = self.get_rect(self.snake[0])
        for i in range(len(apple.rects)):
            if selfRect.colliderect(apple.rects[i]):
                return i

        return -1

    def commited_livent(self):
        headRect = self.get_rect(self.snake[0])
        # print("[HEAD]", headRect)
        dead = 0
        for i in range(1, len(self.snake)):
            rect = self.get_rect(self.snake[i])
            # print(f"[RECT {i}]", rect)
            newDead = headRect.colliderect(rect)
            # print(i, newDead)
            dead = headRect.colliderect(rect) or dead
        return bool(dead)
    def initSnake(self, length):
        startX = WIDTH//2 + length //4
        startY = HEIGHT//2
        l = [(startX - i, startY,) for i in range(length)]
        return l

class Apple():
    def __init__(self):
        self.positions = self.generateApple(1)
        self.rects = self.getRects()

    def show(self, screen):
        for apple in self.rects:
            pg.draw.rect(screen, clr.red, apple)

    def generateApple(self, count, apple_eaten = None):

        if apple_eaten == None:
            l =[]
        else:
            l = [*self.positions]

            x = randint(0, WIDTH - 1) * BLOCKSIZE
            y = randint(0, HEIGHT - 1) * BLOCKSIZE + TOP_OFFSET

            l[apple_eaten] = (x, y)

        while len(l) < count:
            x = randint(0, WIDTH - 1) * BLOCKSIZE
            y = randint(0, HEIGHT - 1) * BLOCKSIZE + TOP_OFFSET
            l.append((x, y))

        return l

    def getRects(self):
        l = []
        for  pos in self.positions:
            l.append(pg.Rect(pos, (BLOCKSIZE, BLOCKSIZE)))

        return l

    def new(self, snake_length, apple_eaten):
        self.positions = self.generateApple(snake_length//8, apple_eaten)
        self.rects = self.getRects()

############################################################################################################################ 

def mainLoop(screencol, textcol, prev_screen = None, rect_pos = None):
    pg.display.set_caption('Snake')
    start = True
    screenWd, screenHt = 1120, 630
    screenCenter = (screenWd//2, screenHt//2)
    screen = pg.display.set_mode((screenWd, screenHt))
    clock = pg.time.Clock()
    FPS = 20
    alive = True
    score = 0
    paused = False
    center = (screenWd //2, 100)

    butt_mode = Button(1075, 15, 20, 20)

    snake = Snake()
    apple = Apple()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # fade(screen, True, col = screencol)
                    return False, screencol, textcol
                if event.key == pg.K_SPACE and alive and paused:
                    paused = False
                elif event.key in MOVES and MOVES[event.key][1] != snake.velocity:
                    snake.velocity = MOVES[event.key][0]
                elif event.key == pg.K_p and alive:
                    if paused:
                        paused = False
                    else:
                        paused = True
                        text(screen, 0, 0, 50, "Paused", textcol, center)
                elif event.key == pg.K_n:
                    return True, screencol, textcol
                elif event.key == pg.K_h and not paused:
                    paused = True
                    fade(screen, True, col = screencol)
                    help_screen(SNAKE, screencol, textcol)
                elif event.key == pg.K_m:
                    if screencol == clr.black:
                        screencol = clr.white
                        textcol = clr.black
                    else:
                        screencol = clr.black
                        textcol = clr.white

        screen.fill(screencol)

        if butt_mode.get_click():
            if screencol == clr.black:
                screencol = clr.white
                textcol = clr.black
            else:
                screencol = clr.black
                textcol = clr.white

        if paused:
            text(screen, 0, 0, 50, "Paused", textcol, center)
        elif not start and alive:
            snake.move()
            apple_eaten = snake.collide(apple)
            if apple_eaten != -1:
                score += 1
                apple.new(len(snake.snake) + 1, apple_eaten)
                snake.snake.append(snake.snake[-1])
            
            if snake.commited_livent():
                alive = False

        if screencol == clr.black:
            sun(screen)
        else:
            moon(screen)

        if alive == False:
            new, home, origin = lose(screen, screenCenter, score)
            if home.get_click(origin):
                fade(screen, True, col = screencol)
                return False, screencol, textcol
            if new.get_click(origin):
                return True, screencol, textcol

        apple.show(screen)
        snake.show(screen, textcol)
        text(screen, screenWd - 70, 5, 30, str(score), textcol)

        if start and prev_screen != None:
            expand(screen, screen.copy(), [rect_pos[0], rect_pos[1]+90, 200, 113], prev_screen)
            start = False
        else:
            pg.display.update()
            clock.tick(FPS)


# try:
#    restart = mainLoop(clr.black, clr.white)
#    while restart[0]:
#        restart = mainLoop(clr.black, clr.white)
# except:
#    traceback.print_exc()
# finally:
#    pg.quit()