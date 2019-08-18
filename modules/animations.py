import pygame as pg
import clr
from math import sin, pi
from statistics import mean

screen_size = (1120, 630)
screen_center = (screen_size[0]//2, screen_size[1]//2)
clock = pg.time.Clock()
FPS = 100

def easeIn(time, start, change, total_time):
    time /= total_time
    return time*time*time*change/11 + start

def sin_curve(dist, iterations):
    # calculates sin values
    l = []
    for i in range(iterations):
        l.append(sin((i+1)*pi/iterations))

    # average of sines
    avg = mean(l)

    # average distance travelled by all value
    avg_iter_dist = dist / avg / iterations

    return l, avg_iter_dist


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

def expand(screen, icon, rect, prev_screen, time = 0.3):
    iterations =  round(FPS * time)
 
    pos = [rect[0], rect[1]]

    size = [rect[2], rect[3]]

    scale_x = screen_size[0] - size[0]
    scale_y = scale_x * 9/16

    pos_diff = (-pos[0], -pos[1])

    for i in range(iterations):

        size[0] = round(easeIn(i, size[0], scale_x, iterations))
        size[1] = round(easeIn(i, size[1], scale_y, iterations))

        blit_icon = pg.transform.smoothscale(icon, size)

        pos[0] = round(easeIn(i, pos[0], pos_diff[0], iterations))
        pos[1] = round(easeIn(i, pos[1], pos_diff[1], iterations))
        screen.blit(prev_screen, (0,0))
        screen.blit(blit_icon, pos)
        pg.display.update()
        clock.tick(FPS)

# def expand2(screen, icon, rect, prev_screen = None, time = 0.5):
#     if prev_screen == None:
#         prev_screen = screen.copy()
 
#     pos = [rect[0], rect[1]]
#     size = [rect[2], rect[3]]

#     iterations =  round(FPS * time)

#     scale_x = round(screen_size[0] - size[0])
#     scale_y = round(scale_x * 9/16)

#     pos_diff = (-pos[0], -pos[1])
    
#     pos_change = (pos_diff[0]//iterations, pos_diff[1]//iterations)

#     scale_x_l, scale_x_avg = sin_curve(scale_x, iterations)
#     scale_y_l, scale_y_avg = sin_curve(scale_y, iterations)

#     pos_l = [None, None]
#     pos_avg = [None, None]
#     pos_l[0], pos_avg[0] = sin_curve(pos_diff[0], iterations)
#     pos_l[1], pos_avg[1] = sin_curve(pos_diff[1], iterations)

#     for i in range(iterations):

#         # screen.fill(clr.white)

#         size[0] += round(scale_x_l[i] * scale_x_avg)
#         size[1] += round(scale_y_l[i] * scale_y_avg)

#         blit_icon = pg.transform.smoothscale(icon, size)

#         pos[0] += round(pos_l[0][i] * pos_avg[0])
#         pos[1] += round(pos_l[1][i] * pos_avg[1])

#         screen.blit(prev_screen, (0,0))
#         screen.blit(blit_icon, pos)
#         pg.display.update()
#         clock.tick(FPS)

# def expand_og(screen, icon, rect, prev_screen = None, time = 0.5):
#     if prev_screen == None:
#         prev_screen = screen.copy()
 
#     pos = [rect[0], rect[1]]
#     size = [rect[2], rect[3]]

#     iterations =  round(FPS * time)

#     scale_x = round((screen_size[0] - size[0])/iterations)
#     scale_y = round(scale_x * 9/16)

    
#     pos_diff = (-pos[0], -pos[1])
    
#     pos_change = (pos_diff[0]//iterations, pos_diff[1]//iterations)

#     for i in range(iterations):

#         # screen.fill(clr.white)

#         size[0] += scale_x
#         size[1] += scale_y

#         blit_icon = pg.transform.smoothscale(icon, size)

#         pos[0] += pos_change[0]
#         pos[1] += pos_change[1]
#         screen.blit(prev_screen, (0,0))
#         screen.blit(blit_icon, pos)
#         pg.display.update()
#         clock.tick(FPS)