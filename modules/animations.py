import pygame as pg
import clr

screen_size = (1120, 630)
screen_center = (screen_size[0]//2, screen_size[1]//2)
clock = pg.time.Clock()
FPS = 60

def fade(screen, begin, time = 0.25, col = clr.black):
    if begin:
        start = 0
        stop = 256
        step = round(256/(FPS * time))
    else:
        start = 256
        stop = 0
        step = -round(256/(FPS * time))
    prev_screen = screen.copy()
    surface = pg.Surface(screen_size)
    surface.fill(col)
    for alpha in range(start, stop, step):
        surface.set_alpha(alpha)
        screen.blit(prev_screen, (0,0))
        screen.blit(surface, (0,0))
        pg.display.update()
        clock.tick(FPS)

def expand(screen, icon, rect, prev_screen = None, time = 0.3):
    if prev_screen == None:
        prev_screen = screen.copy()
 
    pos = [rect[0], rect[1]]
    size = [rect[2], rect[3]]

    iterations =  round(FPS * time)

    scale_x = round((screen_size[0] - size[0])/iterations)
    scale_y = round(scale_x * 9/16)

    pos_diff = (-pos[0], -pos[1])
    
    pos_change = (pos_diff[0]//iterations, pos_diff[1]//iterations)

    for i in range(iterations):

        # screen.fill(clr.white)

        size[0] += scale_x
        size[1] += scale_y

        blit_icon = pg.transform.smoothscale(icon, size)

        pos[0] += pos_change[0]
        pos[1] += pos_change[1]
        screen.blit(prev_screen, (0,0))
        screen.blit(blit_icon, pos)
        pg.display.update()
        clock.tick(FPS)