import pygame as pg
pg.init()
import sys, os
import traceback
from GUI_elements import*
from clr import*

#Classes-------------------------------------------------------------------------------------------------------------

class Canvas():
    def __init__(self, screencol, brushcol, thickness, e_thickness, screenWd, screenHt, pos, butt_undo, butt_redo):
        self.screencol = screencol
        self.brushcol = brushcol
        self.thick = thickness
        self.e_thick = e_thickness
        #modes = b for brush, e - eraser, l - line, r - rectangle, c - circle, el for elipse, f - fill and p - colour picker
        self.mode = 'b'
        self.size = (screenWd - pos[0], screenHt - pos[1])
        self.surf = pg.Surface(self.size)
        self.pos = pos
        # self.pos1 = (370, 100)
        # self.pos2 = (740, 100)
        self.prev_pos = (0,0)
        self.pressed = False
        self.surf2 = pg.Surface(self.size)
        self.surf_swap = 0
        self.current_surf = self.surf
        self.undo = butt_undo
        self.redo = butt_redo
        self.prev_screencol = screencol
        self.tempSurf = None
        self.surflist = [self.surf.copy()]
        self.list_pos = 0
        self.repeat = False
    def fill(self, pos, screen):
        pos = tuple(pos)
        screencol = screen.get_at(pos)
        if self.brushcol == screencol:
            return
        screen.set_at(pos, self.brushcol)
        queue = [pos]
        while len(queue) > 0:
            x,y = queue.pop(0)
            if x-1 >= 0 and screen.get_at((x-1, y)) == screencol: #check if left is still part of canvas and the left pixel should be coloured
                screen.set_at((x-1,y), self.brushcol)
                queue.append((x-1, y))
            if x + 1 < 1120 and screen.get_at((x+1, y)) == screencol:
                screen.set_at((x+1,y), self.brushcol)
                queue.append((x+1, y))
            if y-1 >= 0 and screen.get_at((x, y-1)) == screencol:
                screen.set_at((x,y-1), self.brushcol)
                queue.append((x, y-1))
            if y+1 < 530 and screen.get_at((x, y+1)) == screencol:
                screen.set_at((x,y+1), self.brushcol)
                queue.append((x, y+1))
    def draw(self, screen):
        if self.mode == 'b':
            thick = self.thick
        else:
            thick = self.e_thick
        pos = list(pg.mouse.get_pos())
        pos[0], pos[1] = pos[0] - self.pos[0], pos[1] - self.pos[1]
        if self.pressed == False:
            active(self.undo)
            for i in range(self.list_pos, len(self.surflist)-1):
                self.surflist.pop()
            self.surflist.append(self.surflist[self.list_pos].copy())
            self.list_pos += 1
            self.prev_pos = pos
        if self.mode == 'b':
            col = self.brushcol
        elif self.mode == 'p':
            self.brushcol = self.surflist[self.list_pos].get_at(pos)
            self.mode = 'b'
            self.selected = False
            return
        elif self.mode == 'f':
            self.fill(pos, self.surflist[self.list_pos])
            return
        elif self.mode == 'e':
            col = self.screencol
        else:
            self.pressed = True
            self.tempSurf = pg.Surface(self.size)
            if self.repeat:
                surf = self.surflist[self.list_pos]
            else:
                surf = self.tempSurf
            shape_draw(self, pos, surf)
            return

        pg.draw.line(self.surflist[self.list_pos], col, self.prev_pos, pos, thick)
        self.prev_pos = pos
        self.pressed = True
        self.tempSurf = None
    def show(self, screen):
        #print(self.list_pos, len(self.surflist))
        screen.blit(self.surflist[self.list_pos], self.pos)
        if self.tempSurf != None:
            screen.blit(self.tempSurf, self.pos)
    def new(self, screen, mode_change = True):
        for i in range(len(self.surflist)-1):
            self.surflist.pop()
        self.surflist[0].fill(self.screencol)
        self.list_pos = 0
        active(self.undo, False)
        active(self.redo, False)
        if self.tempSurf != None:
            self.tempSurf.fill(self.screencol)
        self.surf_swap = 0
        if mode_change:
            self.mode = 'b'
    def new_col(self, screen):
        temp_surf = self.surflist[self.list_pos].copy()
        temp_surf.set_colorkey(self.prev_screencol)
        self.new(screen, False)
        self.surflist[self.list_pos].blit(temp_surf, (0,0))

class Slider():
    def __init__(self, pos, screen_pos, col , current_rgb_val, value, height = 20, width = 265):
        self.pos = pos
        self.col = col
        self.ht = height
        self.wd = width
        self.surf = pg.Surface((width, height))
        self.surfRect = self.surf.get_rect()
        self.surfRect[0] = screen_pos[0]
        self.surfRect[1] = screen_pos[1]
        self.screen_pos = screen_pos
        self.cursor = Button(current_rgb_val, (height//2 - 10), 5, 10, hovour = True)
        self.value = value
    def show(self, screen):
        self.surf.fill(light_gray)
        pg.draw.line(self.surf, self.col, (5, self.ht//2), (self.wd-10, self.ht//2), 3)
        self.cursor.show(self.surf)
        screen.blit(self.surf, self.pos)
    def move(self, prev_col):
        mpos = pg.mouse.get_pos()
        if self.surfRect.collidepoint(mpos) and pg.mouse.get_pressed()[0]:
            self.cursor.rect.center = (mpos[0]-self.screen_pos[0],self.ht//2)
            return mpos[0]-self.screen_pos[0], True
        return prev_col, False

###########################################################################################################################################################
def shape_draw(canvas, pos, surf):
    if canvas.tempSurf != None:
        canvas.tempSurf.fill(canvas.screencol)
        canvas.tempSurf.set_colorkey(canvas.screencol)
    if canvas.mode == 'l':
        pg.draw.line(surf, canvas.brushcol, canvas.prev_pos, pos, canvas.thick)
    elif canvas.mode == 'r' or canvas.mode == 'el':
        if pos[0] > canvas.prev_pos[0]:
            wd = pos[0] - canvas.prev_pos[0]
        else:
            wd = canvas.prev_pos[0] - pos[0]
        if pos[1] > canvas.prev_pos[1]:
            ht = pos[1] - canvas.prev_pos[1]
        else:
            ht = canvas.prev_pos[1] - pos[1]
        drawing_rect = pg.Rect(canvas.prev_pos, (wd,ht))
        if pos[0] < canvas.prev_pos[0] and pos[1] < canvas.prev_pos[1]:
            drawing_rect.topleft = pos
        elif pos[0] < canvas.prev_pos[0] and pos[1] > canvas.prev_pos[1]:
            drawing_rect.bottomleft = pos
        elif pos[0] > canvas.prev_pos[0] and pos[1] < canvas.prev_pos[1]:
            drawing_rect.topright = pos
        if canvas.mode == 'r':
            if wd > canvas.thick or ht > canvas.thick:
                thickness = canvas.thick
            else:
                thickness = 0
        if canvas.mode == 'el':
            if wd//2 > canvas.thick and ht//2 > canvas.thick:
                thickness = canvas.thick
            else:
                thickness = 0
        if canvas.mode == 'r':
            pg.draw.rect(surf, canvas.brushcol, drawing_rect, thickness)
        else:
            pg.draw.ellipse(surf, canvas.brushcol, drawing_rect, thickness)
    elif canvas.mode == 'c':
        circ_center = ((pos[0] + canvas.prev_pos[0])//2, (pos[1] + canvas.prev_pos[1])//2)
        r = int(((pos[0] - circ_center[0])**2 + (pos[1]- circ_center[1])**2)**0.5)
        if canvas.thick > r:
            thickness = 0
        else:
            thickness = canvas.thick
        pg.draw.circle(surf, canvas.brushcol, circ_center, r, thickness)

def active(button, mode = True):
    button.activated = mode
    if mode:
        button.textColour = black
    else:
        button.textColour = red
    button.hovour = mode

def rgb_col(screen, canvas, rgb_val, pos):
    count = 0
    clock = pg.time.Clock()
    FPS = 20
    surf = pg.Surface((265, 140))
    surf.fill(light_gray)
    surfRect = surf.get_rect()
    surfRect[0] = pos[0]
    surfRect[1] = pos[1]
    current_col_surf = pg.Surface((265,40))
    current_rgb_text = Text(1, 1, 20, (265, 40), str(rgb_val))
    rgb_val = list(rgb_val)
    while len(rgb_val) > 3:
        rgb_val.pop()

    red_slider = Slider((5, 15), (pos[0]+5, pos[1]+15), red, rgb_val[0], 0)
    green_slider = Slider((5, 40), (pos[0]+5, pos[1]+40), green, rgb_val[1], 1)
    blue_slider =Slider((5, 65), (pos[0]+5, pos[1]+65), blue, rgb_val[2], 2)

    slider_list = [red_slider, green_slider, blue_slider]
    last_clicked = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                if event.key == pg.K_RETURN:
                    return rgb_val

        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            temp_pos = list(slider_list[last_clicked].cursor.rect.center)
            temp_pos [0] -= 1
            slider_list[last_clicked].cursor.rect.center = temp_pos
            rgb_val[last_clicked] = slider_list[last_clicked].cursor.rect.center[0]
        if keystate[pg.K_RIGHT]:
            temp_pos = list(slider_list[last_clicked].cursor.rect.center)
            temp_pos [0] += 1
            slider_list[last_clicked].cursor.rect.center = temp_pos
            rgb_val[last_clicked] = slider_list[last_clicked].cursor.rect.center[0]

        dark_count = 0
        for i in rgb_val:
            if i < 100:
                dark_count += 1
        if dark_count == 3:
            current_rgb_text.colour = white
        else:
            current_rgb_text.colour = black

        for i in range(len(slider_list)):
            slider_list[i].show(surf)
            rgb_val[i], clicked = slider_list[i].move(rgb_val[i])
            if clicked:
                last_clicked = slider_list[i].value

        current_rgb_text.text = str(rgb_val)
        for i in range(3):
            if rgb_val[i] > 255:
                rgb_val[i] = 255
            elif rgb_val[i] < 0:
                rgb_val[i] = 0
        if pg.mouse.get_pressed()[0] and (surfRect.collidepoint(pg.mouse.get_pos()) == False) and count>40:
            return rgb_val
        current_col_surf.fill(pg.Color(rgb_val[0], rgb_val[1], rgb_val[2]))
        current_rgb_text.display(current_col_surf)
        surf.blit(current_col_surf, (0, 100))
        screen.blit(surf, pos)
        pg.display.update()
        count+=1
        clock.tick(FPS)

def colchoice(screen, canvas, canvas_col_button):
    rgb_val = list(canvas.screencol)
    clock = pg.time.Clock()
    FPS = 25
    count = 0
    surf = pg.Surface((100, 265))
    surf.fill(light_gray)
    surfRect = surf.get_rect()
    surfRect[0] = 745
    surfRect[1] = 105

    while len(rgb_val) > 3:
        rgb_val.pop()
    
    templist = [i for i in range(8)]
    templist[0] = Button(12, 12, 25, 25, colour = white,surfpos = (745, 105), outline = True, hovour = False)
    templist[1] = Button(63, 12, 25, 25, colour = black, surfpos = (745, 105), outline = True, hovour = False)
    templist[2] = Button(12, 62, 25, 25, colour = red, surfpos = (745, 105), outline = True, hovour = False)
    templist[3] = Button(63, 62, 25, 25, colour = orange, surfpos = (745, 105), outline = True, hovour = False)
    templist[4] = Button(12, 112, 25, 25, colour = yellow, surfpos = (745, 105), outline = True, hovour = False)
    templist[5] = Button(63, 112, 25, 25, colour = green, surfpos = (745, 105), outline = True, hovour = False)
    templist[6] = Button(12, 162, 25, 25, colour = sky, surfpos = (745, 105), outline = True, hovour = False)
    templist[7] = Button(63, 162, 25, 25, colour = blue, surfpos = (745, 105), outline = True, hovour = False)
    rgb = Button(25, 205, 50, 50, 'RGB', textHeight = 30, colour = canvas.screencol, surfpos = (745, 105), outline = True, hovour = False)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
        for button in templist:
            if button.get_click():
                canvas.prev_screencol = canvas.screencol
                canvas.screencol = button.colour
                canvas.new_col(screen)
                canvas_col_button.colour = button.colour
                return
            button.show(surf)
        if pg.mouse.get_pressed()[0] and surfRect.collidepoint(pg.mouse.get_pos()) == False and count>10:
            return
        if rgb.get_click():
            rgb_val = rgb_col(screen, canvas, rgb_val, (662, 375))
            if rgb_val != None:
                canvas.prev_screencol = canvas.screencol
                canvas.screencol = pg.Color(rgb_val[0], rgb_val[1], rgb_val[2])
                canvas.new_col(screen)
                canvas_col_button.colour = canvas.screencol
        rgb.show(surf)
        screen.blit(surf, (745, 105))
        pg.display.update()
        count += 1
        clock.tick(FPS)

def shape_choice(screen, canvas, surfpos = (975, 105)):
    clock = pg.time.Clock()
    FPS = 20
    surf = pg.Surface((80, 320))
    count = 0
    surfRect = surf.get_rect()
    surfRect [0], surfRect[1] = surfpos[0], surfpos[1]


    line_surf = pg.Surface((40, 40))
    line_surf.fill(light_gray)
    pg.draw.line(line_surf, canvas.brushcol, (5, 5), (35, 35), 2)

    rect_surf = pg.Surface((40, 40))
    rect_surf.fill(light_gray)
    pg.draw.rect(rect_surf, canvas.brushcol, (5, 10, 30, 20), 2)

    circ_surf = pg.Surface((40, 40))
    circ_surf.fill(light_gray)
    pg.draw.circle(circ_surf, canvas.brushcol, (20, 20), 15, 2)

    ellipse_surf = pg.Surface((40, 40))
    ellipse_surf.fill(light_gray)
    pg.draw.ellipse(ellipse_surf, canvas.brushcol, (5, 10, 30, 20), 2)


    line_button = Button(20, 20, 40, 40, img = line_surf, value = 'l', surfpos = surfpos, outline = True, hovour = False)
    rect_button = Button(20, 80, 40, 40, img = rect_surf, value = 'r', surfpos = surfpos, outline = True, hovour = False)
    circ_button = Button(20, 140, 40, 40, img = circ_surf, value = 'c', surfpos = surfpos, outline = True, hovour = False)
    elps_button = Button(20, 200, 40, 40, img = ellipse_surf, value = 'el', surfpos = surfpos, outline = True, hovour = False)
    rep_button = Button(20, 260, 40, 40, "repeat", textHeight = 15, colour = light_gray, hovourColour = light_light_gray, surfpos = surfpos, outline = True)

    button_list = [line_button, rect_button, circ_button, elps_button]

    if canvas.repeat:
        rep_button.selected = True

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

        surf.fill(light_gray)
        for button in button_list:
            if button.get_click():
                canvas.mode = button.value
                return
            if canvas.mode == button.value:
                button.selected = True
            button.show(surf)

        if pg.mouse.get_pressed()[0] and surfRect.collidepoint(pg.mouse.get_pos()) == False and count > 20:
            return

        if rep_button.get_click():
            if canvas.repeat:
                canvas.repeat = False
                rep_button.selected = False
            else:
                canvas.repeat = True
                rep_button.selected = True

        rep_button.show(surf)

        screen.blit(surf, surfpos)
        pg.display.update()
        count += 1
        clock.tick(FPS)

def brushsize(screen, canvas):
    clock = pg.time.Clock()
    FPS = 20
    surf = pg.Surface((100, 50))
    count = 0
    surfRect = surf.get_rect()

    dct = {pg.K_1:1, pg.K_2:2, pg.K_3:3, pg.K_4:4, pg.K_5:5, pg.K_6:6, pg.K_7:7, pg.K_8:8, pg.K_9:9, pg.K_0:0}
    text_size = Text(0, 30, 25, surfRect.size, str(canvas.thick))
    text_instructions = Text(0, 10, 15, surfRect.size, "Type Size in pixels")
    check = True

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                if check:
                    text_size.text = ''
                    check = False
                if event.key in dct:
                    text_size.text += str(dct[event.key])
                elif event.key == pg.K_RETURN:
                    canvas.thick = int(text_size.text)
                    canvas.e_thick = int(text_size.text) + 25
                    return
                elif event.key == pg.K_EQUALS:
                    canvas.thick = int(text_size.text)
                    canvas.e_thick = int(text_size.text) + 25
                    return
                elif event.key == pg.K_BACKSPACE:
                    text_size.text = text_size.size[:-1]


        if pg.mouse.get_pressed()[0] and surfRect.collidepoint(pg.mouse.get_pos()) == False and count>40:
            return
        surf.fill(light_gray)
        text_instructions.display(surf)
        text_size.display(surf)
        screen.blit(surf, (450, 105))
        pg.display.update()
        count += 1
        clock.tick(FPS)

def toolbar(screen, button_list_col, button_list_mode, button_list_misc, canvas, size = (1120, 100), pos = (0,0), col = light_gray):
    rgb_val = canvas.brushcol
    surf = pg.Surface(size)
    surf.fill(col)
    for button in button_list_col:
            if button.get_click():
                rgb_val = button.colour
                canvas.brushcol = button.colour
                button.selected = True
                if canvas.mode == 'e':
                    canvas.mode = 'b'
                if canvas.brushcol == canvas.screencol:
                    canvas.mode = 'e'
            if button.selected and canvas.brushcol != button.colour:
                button.selected = False
            button.show(surf)
    for button in button_list_mode:
            if button.get_click():
                canvas.mode = button.value
                if canvas.mode == button.value:
                    button.selected = True
            if button.selected and canvas.mode != button.value:
                button.selected = False
            button.show(surf)

    if button_list_misc[0].get_click():
        canvas.new(screen)
    elif button_list_misc[1].get_click():
        canvas.list_pos -= 1
        if canvas.list_pos == 0:
            active(button_list_misc[1], False)
        active(button_list_misc[2])
        canvas.show(screen)
    elif button_list_misc[2].get_click():
        canvas.list_pos += 1
        if canvas.list_pos == len(canvas.surflist) - 1:
            active(button_list_misc[2], False)
        active(button_list_misc[1])
    for button in button_list_misc:
        button.show(surf, canvas = canvas)
    screen.blit(surf, pos)
    if button_list_misc[3].get_click():
        colchoice(screen, canvas, button_list_misc[3])
        if canvas.screencol == canvas.brushcol:
            canvas.mode = 'e'
    elif button_list_misc[4].get_click():
        brushsize(screen, canvas)
    elif button_list_misc[5].get_click():
        rgb_val = rgb_col(screen, canvas, rgb_val, (492, 105))
        if rgb_val != None:
            canvas.brushcol = pg.Color(rgb_val[0], rgb_val[1], rgb_val[2])
        if canvas.brushcol == canvas.screencol:
            canvas.mode = 'e'
    elif button_list_misc[6].get_click():
        shape_choice(screen, canvas)
        pg.time.wait(10)

def mainLoop(screencol, brushcol, prev_screen, rect_pos):
    start = True
    pg.display.set_caption('Paint')
    screenWd, screenHt = (1120, 630)
    screen = pg.display.set_mode((screenWd, screenHt))
    FPS = 50
    draw_frames = 1000
    count = 0
    frames = draw_frames//FPS
    clock = pg.time.Clock()

    white_butt = Button(250, 12, 25, 25, colour = white, outline = True, hovour = False)
    black_butt = Button(250, 63, 25, 25, colour = black, outline = True, hovour = False)
    red_butt = Button(300, 12, 25, 25, colour = red, outline = True, hovour = False)
    orange_butt = Button(300, 63, 25, 25, colour = orange, outline = True, hovour = False)
    yellow_butt = Button(350, 63, 25, 25, colour = yellow, outline = True, hovour = False)
    green_butt = Button(350, 12, 25, 25, colour = green, outline = True, hovour = False)
    skyblue_butt = Button(400, 63, 25, 25, colour = sky, outline = True, hovour = False)
    blue_butt = Button(400, 12, 25, 25, colour = blue, outline = True, hovour = False)
    
    butt_undo = Button(700, 30, 40, 40, "<---", colour = light_gray, hovourColour = white,
        textHeight = 30,  enabled_selected = False, outline = True, activated = False)
    butt_redo = Button(760, 30, 40, 40, "--->", colour = light_gray, hovourColour = white,
        textHeight = 30,  enabled_selected = False, outline = True, activated = False)

    canvas = Canvas(screencol, brushcol, 5, 30, screenWd, screenHt, (0,100), butt_undo, butt_redo)
    canvas.new(screen)

    brush = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "brush.png"))
    brush_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "brush_hov.png"))
    eraser = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "eraser.png"))
    slider = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "slider.jpeg"))
    eraser_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "eraser_hov.png"))
    col_pick_pic = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "col_pick.png"))
    col_pick_pic_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "col_pick_hov.png"))
    fill_pic = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "fill.png"))
    fill_pic_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "fill.jpeg"))
    
    shapes_surf = pg.Surface((50, 50))
    shapes_surf.fill(light_gray)
    pg.draw.circle(shapes_surf, black, (25, 25), 15, 2)
    shapes_surf_hov = pg.Surface((50, 50))
    shapes_surf_hov.fill(white)
    pg.draw.circle(shapes_surf_hov, black, (25, 25), 15, 2)
    

    brush_butt = Button(100,25, 50, 50, img = brush, hovourImg = brush_hov, hovour = True, value = 'b', outline = True)
    eraser_butt = Button(175,25, 50, 50, img = eraser, hovourImg = eraser_hov, hovour = True, value = 'e', outline = True)
    butt_col_pick = Button(900, 25, 50, 50, value = 'p', img = col_pick_pic, hovourImg = col_pick_pic_hov, outline = True)
    butt_fill = Button(975, 25, 50, 50, value = 'f', img = fill_pic, hovourImg = fill_pic_hov, outline = True)
    
    butt_new = Button(25, 25, 50, 50, 'new', textHeight = 30,colour = white, enabled_selected = False, outline = True, hovour = False)
    butt_canvas_menu = Button(835, 30, 40, 40, colour = canvas.screencol, enabled_selected = False, outline = True, hovour = False)
    butt_size = Button(450, 25, 100, 50, colour = light_gray, enabled_selected = False, isSize = True, hovour = False)
    butt_slider = Button(575, 25, 100, 50, img = slider, enabled_selected = False, outline = True, hovour = False)
    butt_shapes = Button(1050, 25, 50, 50, img = shapes_surf, hovourImg = shapes_surf_hov, outline = True)

    button_list_col = [white_butt, black_butt, red_butt, orange_butt, yellow_butt,
                            green_butt, skyblue_butt, blue_butt]
    button_list_mode = [brush_butt, eraser_butt, butt_col_pick, butt_fill]
    button_list_misc = [butt_new, butt_undo, butt_redo, butt_canvas_menu, butt_size, butt_slider, butt_shapes]

    if screencol == black:
        white_butt.selected = True
    else:
        black_butt.selected = True
    brush_butt.selected = True

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fade(screen, True, col = screencol)
                    return

        mpos = pg.mouse.get_pos()

        if mpos[0] > canvas.pos[0] and mpos[1] > canvas.pos[1]:
            if pg.mouse.get_pressed()[0]:
                if canvas.mode == 'p':
                    brush_butt.selected = True
                canvas.draw(screen)
            else:
                if canvas.pressed == True:
                    pos = (mpos[0], mpos[1] - 100)
                    shape_draw(canvas, pos, canvas.surflist[canvas.list_pos])
                canvas.pressed = False
            pg.mouse.set_visible(False)
        else:
            canvas.pressed = False
            pg.mouse.set_visible(True)

        if count % frames == 0:

            screen.fill(screencol)

            canvas.show(screen)

            if canvas.mode == 'e':
                rect = pg.Rect(mpos, (canvas.e_thick, canvas.e_thick))
                rect.center = mpos
                pg.draw.rect(screen, canvas.screencol, rect)
                pg.draw.rect(screen, black, rect, 1)
            elif canvas.mode == 'f':
                pg.draw.circle(screen, canvas.brushcol, mpos, 2)
            elif canvas.mode == 'p':
                pg.draw.circle(screen, screen.get_at(mpos), mpos, 10)
                pg.draw.circle(screen, black, mpos, 10, 1)
            else:
                pg.draw.circle(screen, canvas.brushcol, mpos, canvas.thick//2)

            toolbar(screen, button_list_col, button_list_mode, button_list_misc, canvas)
            
            if start:
                expand(screen, screen.copy(), [rect_pos[0], rect_pos[1]+87, 200, 113], prev_screen)
                start = False
            else:
                pg.display.update()
        count += 1
        clock.tick(draw_frames)

# try:
#     mainLoop(white, black)
# except:
#     traceback.print_exc()
# finally:
#     Quit()