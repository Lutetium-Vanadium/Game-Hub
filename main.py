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
textCol = clr.white
screenCol = clr.black


pg.display.set_caption('Hub')

###################################################################################################################################################################################################

def mainLoop():
    global textCol, screenCol
    screenWd, screenHt = 1120, 630
    screen = pg.display.set_mode((screenWd, screenHt))
    clock = pg.time.Clock()
    FPS = 25
    background = black_background = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "background.png"))
    white_background = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "white_background.png"))
    randGameImage = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "randGame.png"))
    randGameImage_hovour =pg.image.load(os.path.join(os.getcwd(), "python_pictures", "randGame_hovour.png"))
    paintImg = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "paint_icon.png"))
    paintImg_hovour =pg.image.load(os.path.join(os.getcwd(), "python_pictures", "paint_icon_hov.png"))
    tictactoe_image = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "tictactoe.png"))
    tictactoe_hovour = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "tictactoe_hovour.png"))
    flappybird_img = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "bird_icon.png"))
    flappybird_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "bird_icon_hovour.png"))
    dinorun_img = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_icon.png"))
    dinorun_img_hov = pg.image.load(os.path.join(os.getcwd(), "python_pictures", "dino_icon_hover.png"))

    randCircle = Button(50, 50, 200, 200, 'Circle Game', randGameImage, randGameImage_hovour, textColour = clr.white)
    paint_button = Button(50, 325, 200, 200, '', paintImg, paintImg_hovour, textColour = clr.white)
    tictactoe_button = Button(320, 50, 200, 200, 'Tic-Tac-Toe', tictactoe_image, tictactoe_hovour)
    flappybird = Button(590, 50, 200, 200, 'Flappy Bird', flappybird_img, flappybird_hov)
    dino_run = Button(860, 50, 200, 200, 'Dino run', dinorun_img, dinorun_img_hov)

    exit_button = Button(1050, 600, 50, 30, "Exit", textHeight = 30, textColour = clr.white, opaque = False)
    butt_mode = Button(1075, 15, 20, 20)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit()

        if randCircle.get_click():
            temp = screenCol
            screenCol, textCol, speed, size = randGameHub.difficultyChoice(screenCol, textCol)
            if speed:
                screenCol, textCol = randGameHub.mainLoop(screenCol, textCol, speed, size)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol

        elif paint_button.get_click():
            paint.mainLoop(screenCol, textCol)
            pg.mouse.set_visible(True)

        elif tictactoe_button.get_click():
            temp = screenCol
            screenCol, textCol = tictactoe.mainLoop(screenCol, textCol)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol

        elif flappybird.get_click():
            temp = screenCol
            replay, screenCol, textCol = flappy_bird.mainLoop(screenCol, textCol)
            while replay:
                replay, screenCol, textCol = flappy_bird.mainLoop(screenCol, textCol)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol

        elif dino_run.get_click():
            temp = screenCol
            replay, screenCol, textCol = dinorun.mainLoop(screenCol, textCol)
            while replay:
                replay, screenCol, textCol = dinorun.mainLoop(screenCol, textCol)
            if temp != screenCol:
                if screenCol == clr.black:
                    background = black_background
                    exit_button.textColour = textCol
                else:
                    background = white_background
                    exit_button.textColour = textCol

        elif exit_button.get_click():
            Quit()

        elif butt_mode.get_click():
            if screenCol == clr.black:
                background = white_background
                exit_button.textColour = textCol = clr.black
                screenCol = clr.white
            else:
                background = black_background
                exit_button.textColour = textCol = clr.white
                screenCol = clr.black

        pg.display.set_caption('Hub')

        screen.blit(background, (0, 0))

        if randCircle.onButton():
            text(screen, 30, 585, 30, "Circle Game: Click on the red circle to win the game!", textCol)
        elif paint_button.onButton():
            text(screen, 30, 585, 30, "Paint: Feel free to draw anything.", textCol)
        elif tictactoe_button.onButton():
            text(screen, 30, 585, 30, "Tic-Tac-Toe: Classic game where you need to get 3 in a row. With 2-player and 1 player.", textCol)
        elif flappybird.onButton():
            text(screen, 30, 585, 30, "Flappy Bird: Classic game where you need to last as long as you can without crashing.", textCol)
        elif dino_run.onButton():
            text(screen, 30, 585, 30, "Dino Run: Classic game where you need to last as long as you can without crashing.", textCol)

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
        pg.display.update()

        clock.tick(FPS)




###################################################################################################################################################################################################

mainLoop()
