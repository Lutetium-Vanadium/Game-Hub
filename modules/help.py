import pygame as pg
import clr
from GUI_elements import*
screenWd, screenHt = 1120, 630
wd_center = screenWd//2
clock = pg.time.Clock()
FPS = 25

HUB = 0
CIRCLE_GAME = 1
TICTACTOE = 2
FLAPPY_BIRD = 3
DINO_RUN = 4
PAINT = 5
MINESWEEPER = 6
PONG = 7
SNAKE = 8

def appName(program):
    if program == HUB:
        return 'Hub'
    elif program == CIRCLE_GAME:
        return 'Circle Game'
    elif program == TICTACTOE:
        return 'Tic-Tac-Toe'
    elif program == FLAPPY_BIRD:
        return 'Flappy Bird'
    elif program == DINO_RUN:
        return 'Dino Run'
    elif program == PAINT:
        return 'Paint'
    elif program == MINESWEEPER:
        return "Minesweeper"
    elif program == PONG:
        return 'Pong'
    elif program == SNAKE:
        return 'Snake'

def help_screen(program, screencol, textcol):
    start = True
    pg.display.set_caption("Help")
    screen = pg.display.set_mode((screenWd, screenHt))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit(screen)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fade(screen, True, col = screencol)
                    pg.display.set_caption(appName(program))
                    return
                if event.key == pg.K_RETURN:
                    fade(screen, True, col = screencol)
                    pg.display.set_caption(appName(program))
                    return
        if pg.mouse.get_pressed()[0]:
            fade(screen, True, col = screencol)
            pg.display.set_caption(appName(program))
            return

        screen.fill(screencol)

        text(screen, 0, 0, 40, 'Shortcuts', textcol, (wd_center, 50))
        text(screen, 50, 110, 30, "'n' - Press 'n' for a new game(not applicable to the circle game).", textcol)
        text(screen, 50, 150, 30, "'esc' - Press 'esc' to return to Main Menu. Pressing escape in main menu will quit the program.", textcol)
        text(screen, 50, 190, 30, "'h' - Press 'h' for help(this menu).", textcol)
        text(screen, 50, 230, 30, "'p' - Press 'p' to pause games that can be paused.", textcol)
        text(screen, 50, 270, 30, "'m' - Press 'm' to change light mode or dark mode. Alternatively, click the button in the top right corner.", textcol)
        text(screen, 0, 0, 40, "App specific", textcol, (wd_center, 350))
        s1 = s2 = s3 = ""
        if program == HUB:
            s1 = "Choose which application you want to enter."
            s2 = "Hover over apps to find out what they are."
        elif program == CIRCLE_GAME:
            s1 = "Choose a difficulty and then click the red circle to win."
            s2 = "This game can be paused"
        elif program == TICTACTOE:
            s1 = "Choose 1 player or 2 player. If you have chosen 1 player, you can select difficutly."
            s2 = "Click on the boxes or alternatively press 1-9(in the same order as a number pad) to mark the boxes"
        elif program == FLAPPY_BIRD:
            s1 = "Press spacebar to get acceleration."
            s2 = "This game can be paused."
        elif program == DINO_RUN:
            s1 = "Press spacebar to jump."
            s2 = "This game can be paused."
        elif program == PAINT:
            s1 = "Hover over a tool to find out what it does."
            s2 = "Press 'x' to toggle tool tips."
        elif program == MINESWEEPER:
            s1 = "Left click to reveal a square and right click to place a flag."
            s2 = "If you click on an already revealed square, it reveals surrounding squares."
            s3 = "Click the settings button to change the size and number of bombs."
        elif program == PONG:
            s1 = "Dont let the ball get past your paddle."
            s2 = "'w' and 's' for Player 1 movement. Up and Down arrow for Player 2."
            s3 = "This game can be paused. Press 'r' to restart the round."
        elif program == SNAKE:
            s1 = "Eat apples to increase the length of your snake and your score."
            s2 = "Use arrow keys to move around, turning directly back is prohibited."
            s3 = "Don't collide with yourself or else you'll die."
        text(screen, 50, 380, 30, s1, textcol)
        text(screen, 50, 420, 30, s2, textcol)
        text(screen, 50, 460, 30, s3, textcol)
        text(screen, 0, 0, 30, "Press esc, enter or click anywhere to return.", textcol, (wd_center, 550))

        if start:
            fade(screen, False, col = screencol)
            start = False
        else:
            pg.display.update()
        clock.tick(FPS)
