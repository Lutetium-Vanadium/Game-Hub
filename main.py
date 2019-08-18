import pygame as pg
pg.init()
import os, sys
sys.path.append(os.path.join(os.getcwd(), "modules"))
sys.path.append(os.path.join(os.getcwd(), "python_pictures"))
from GUI_elements import*
import clr
import paint
import tictactoe
import flappy_bird
import dinorun
import randGameHub
import minesweeper
import pong
from help import*
textCol = clr.white
screenCol = clr.black
screenWd, screenHt = 1120, 630
clock = pg.time.Clock()
FPS = 25
SETTINGS = None
hub = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "hub.png"))

def backToHub():
    pg.display.set_caption('Hub')
    pg.display.set_icon(hub)
    return True

###################################################################################################################################################################################################

def mainLoop():
    global textCol, screenCol, back
    screen = pg.display.set_mode((screenWd, screenHt))
    back = False

    background = black_background = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "background.png"))
    white_background = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "white_background.png"))
    
    randGameImage_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "randGame.png"))
    randGameImage = pg.transform.smoothscale(randGameImage_icon, (200, 200))
    randGameImage_hovour =pg.image.load(os.path.join(os.getcwd(), "python_pictures", "randGame_hovour.png"))
    
    paintImg_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "paint_icon.png"))
    paintImg = pg.transform.smoothscale(paintImg_icon, (200, 200))
    paintImg_hovour =pg.image.load(os.path.join(os.getcwd(), "python_pictures", "paint_icon_hov.png"))
    
    tictactoe_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "tictactoe.png"))
    tictactoe_image = pg.transform.smoothscale(tictactoe_icon, (200, 200))
    tictactoe_hovour = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "tictactoe_hovour.png"))
    
    flappybird_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "bird_icon.png"))
    flappybird_img = pg.transform.smoothscale(flappybird_icon, (200, 200))
    flappybird_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "bird_icon_hovour.png"))
    
    dinorun_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_icon.png"))
    dinorun_img = pg.transform.smoothscale(dinorun_icon, (200, 200))
    dinorun_img_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_icon_hover.png"))
    
    mine_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "minesweeper.png"))
    mine_img = pg.transform.smoothscale(mine_icon, (200, 200))
    mine_img_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "minesweeper_hov.png"))

    pong_icon = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "pongImg.png"))
    pong_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "pongImg_hov.png"))

    randCircle = Button(50, 50, 200, 200, 'Circle Game', randGameImage, randGameImage_hovour, textColour = clr.white)
    tictactoe_button = Button(320, 50, 200, 200, 'Tic-Tac-Toe', tictactoe_image, tictactoe_hovour)
    flappybird = Button(590, 50, 200, 200, 'Flappy Bird', flappybird_img, flappybird_hov)
    dino_run = Button(860, 50, 200, 200, 'Dino run', dinorun_img, dinorun_img_hov)
    paint_button = Button(50, 325, 200, 200, '', paintImg, paintImg_hovour)
    mine_button = Button(320, 325, 200, 200, 'minesweeper', mine_img, mine_img_hov, textColour = clr.white)
    pong_button = Button(590, 325, 200, 200, 'pong', pong_icon, pong_hov, textColour = clr.white)

    exit_button = Button(1050, 600, 50, 30, "Exit", textHeight = 30, textColour = textCol, opaque = False)
    butt_mode = Button(1075, 15, 20, 20)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit(screen)
                if event.key == pg.K_m:
                    if screenCol == clr.black:
                        background = white_background
                        exit_button.textColour = textCol = clr.black
                        screenCol = clr.white
                    else:
                        background = black_background
                        exit_button.textColour = textCol = clr.white
                        screenCol = clr.black
                elif event.key == pg.K_h:
                    fade(screen, True, col = screenCol)
                    help_screen(HUB, screenCol, textCol)
<<<<<<< HEAD
                    back = True
=======
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e
        
        if randCircle.get_click():
            temp = screenCol
            pg.display.set_icon(randGameImage)
            screenCol, textCol, speed, size = randGameHub.difficultyChoice(screenCol, textCol, screen.copy(),
                                                                            (randCircle.rect[0], randCircle.rect[1]))
            if speed:
                screenCol, textCol = randGameHub.mainLoop(screenCol, textCol, speed, size)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol
<<<<<<< HEAD
            back = backToHub()
=======
            backToHub()
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e

        elif tictactoe_button.get_click():
            pg.display.set_icon(tictactoe_image)
            temp = screenCol
            screenCol, textCol = tictactoe.mainLoop(screenCol, textCol, screen.copy(),
                                                    (tictactoe_button.rect[0], tictactoe_button.rect[1]))
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol
<<<<<<< HEAD
            back = backToHub()
=======
            backToHub()
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e

        elif flappybird.get_click():
            pg.display.set_icon(flappybird_img)
            temp = screenCol
            replay, screenCol, textCol = flappy_bird.mainLoop(screenCol, textCol, screen.copy(), (flappybird.rect[0], flappybird.rect[1]))
            while replay:
                replay, screenCol, textCol = flappy_bird.mainLoop(screenCol, textCol)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol
<<<<<<< HEAD
            back = backToHub()
=======
            backToHub()
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e

        elif dino_run.get_click():
            pg.display.set_icon(dinorun_img)
            temp = screenCol
            replay, screenCol, textCol = dinorun.mainLoop(screenCol, textCol, screen.copy(), (dino_run.rect[0], dino_run.rect[1]))
            while replay:
                replay, screenCol, textCol = dinorun.mainLoop(screenCol, textCol)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol
<<<<<<< HEAD
            back = backToHub()

        elif paint_button.get_click():
            pg.display.set_icon(paintImg_icon)
            prev_screen = paint.mainLoop(screenCol, textCol, screen.copy(), (paint_button.rect[0], paint_button.rect[1]))
=======
            backToHub()

        elif paint_button.get_click():
            pg.display.set_icon(paintImg_icon)
            paint.mainLoop(screenCol, textCol, screen.copy(), (paint_button.rect[0], paint_button.rect[1]))
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e
            pg.mouse.set_visible(True)
            back = backToHub()

        elif mine_button.get_click():
            pg.display.set_icon(mine_icon)
            temp = screenCol
            n_bombs = 16
            size = (12, 9)
            replay, screenCol, textCol = minesweeper.mainLoop(screenCol, textCol, size, n_bombs, screen.copy(),
                                                                (mine_button.rect[0], mine_button.rect[1]), False)
            if replay == SETTINGS:
                size, n_bombs, screenCol, textCol = minesweeper.settings(screenCol, textCol, size, n_bombs)
                replay = True
            while replay:
                replay, screenCol, textCol = minesweeper.mainLoop(screenCol, textCol, size, n_bombs)
                if replay == SETTINGS:
                    size, n_bombs, screenCol, textCol = minesweeper.settings(screenCol, textCol, size, n_bombs)
                    replay = True
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol
<<<<<<< HEAD
            back = backToHub()
=======
            backToHub()
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e

        elif pong_button.get_click():
            pg.display.set_icon(pong_icon)
            temp = screenCol
            replay, screenCol, textCol = pong.mainLoop(screenCol, textCol, screen.copy(), (pong_button.rect[0], pong_button.rect[1]))
            while replay:
                replay, screenCol, textCol = pong.mainLoop(screenCol, textCol)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol
<<<<<<< HEAD
            back = backToHub()
=======
            backToHub()
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e

        elif exit_button.get_click():
            Quit(screen)

        elif butt_mode.get_click():
            if screenCol == clr.black:
                background = white_background
                exit_button.textColour = textCol = clr.black
                screenCol = clr.white
            else:
                background = black_background
                exit_button.textColour = textCol = clr.white
                screenCol = clr.black

<<<<<<< HEAD
=======
        elif back:
            back = False

>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e
        screen.blit(background, (0, 0))

        if randCircle.onButton():
            s = "Circle Game: Click on the red circle to win the game!"
        elif paint_button.onButton():
            s = "Paint: Feel free to draw anything."
        elif tictactoe_button.onButton():
            s = "Tic-Tac-Toe: Classic game where you need to get 3 in a row. With 2-player and 1 player."
        elif flappybird.onButton():
            s = "Flappy Bird: Classic game where you need to last as long as you can without crashing."
        elif dino_run.onButton():
            s = "Dino Run: Classic game where you need to last as long as you can without crashing."
        elif mine_button.onButton():
            s = "Minesweeper: Win the game by putting flags on every bomb."
        elif pong_button.onButton():
            s = "Pong: Dont let the ball get past you."
        else:
            s = ''
        text(screen, 30, 570, 30, s, textCol)
        text(screen, 0, 0, 25, "Press 'h' for the help.", textCol, (560, 615))

        if screenCol == clr.black:
            sun(screen)
        else:
            moon(screen)

        randCircle.show(screen)
        paint_button.show(screen)
        tictactoe_button.show(screen)
        flappybird.show(screen)
        exit_button.show(screen)
        dino_run.show(screen)
        mine_button.show(screen)
        pong_button.show(screen)

        if back:
            fade(screen, False, col = screenCol)
<<<<<<< HEAD
            pg.display.update()
            # expand(screen, prev_screen, [0, 0, screenWd, screenHt], screen.copy(), False, (paint_button.rect[0], paint_button.rect[1]+87), (200 ,113))
            back = False
=======
>>>>>>> c1f4ac94e85ecdf8bab6a2161d7265f78f99839e
        else:
            pg.display.update()

        clock.tick(FPS)




###################################################################################################################################################################################################

backToHub()
mainLoop()