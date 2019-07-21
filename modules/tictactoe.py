import pygame as pg
pg.init()
from GUI_elements import*
import clr, traceback
from random import choice, randint

##############################################################################################################################################################################################

class Grid():
    def __init__(self, size, x = 0, y = 0, col = clr.black):
        self.box_size = size//3
        self.size = size
        self.coord = (x, y)
        self.col = col
        i = j = 0
        self.boxlist = [[((i*self.box_size+x), (j*self.box_size+y)) for i in range(3)] for j in range(3)]
        self.rectlist = []
        self.box_used = [False for i in range(9)]
        self.flag = False
        for lst in self.boxlist:
            for point in lst:
                self.rectlist.append(pg.Rect(point, (self.box_size, self.box_size)))
    def show(self, screen):
        pg.draw.line(screen, self.col, self.boxlist[1][0], (self.boxlist[1][0][0]+self.size, self.boxlist[1][0][1]), 5)
        pg.draw.line(screen, self.col, self.boxlist[2][0], (self.boxlist[2][0][0]+self.size, self.boxlist[2][0][1]), 5)
        pg.draw.line(screen, self.col, self.boxlist[0][1], (self.boxlist[0][1][0], self.boxlist[0][1][1]+self.size), 5)
        pg.draw.line(screen, self.col, self.boxlist[0][2], (self.boxlist[0][2][0], self.boxlist[0][2][1]+self.size), 5)
    def get_click(self, turn, screen, screenCol):
        pos = pg.mouse.get_pos()
        for i in range(len(self.rectlist)):
            temp = self.rectlist[i].collidepoint(pos) and pg.mouse.get_pressed()[0]
            if temp and not self.flag and not self.box_used[i]:
                if turn%2 == 0:
                    self.box_used[i] = 1
                else:
                    self.box_used[i] = 2
                self.mark(i, turn, screen, screenCol)
                self.flag = True
                return True
            if self.flag and not temp:
                self.flag = False
        return False
    def mark(self, i, turn, screen, screenCol):
        #print(self.rectlist[i][0])
        #print(self.rectlist[i][1])
        surfsize = self.box_size//2
        surf = pg.Surface((surfsize, surfsize))
        surf.fill(screenCol)
        if self.box_used[i] == 1:
            pg.draw.line(surf, clr.red, (0, 0), (surfsize, surfsize), 5)
            pg.draw.line(surf, clr.red, (0, surfsize), (surfsize, 0), 5)
        elif self.box_used[i] == 2:
            r = surfsize//2
            pg.draw.circle(surf, clr.blue, (r, r), r, 5)
        #print(self.box_used)
        screen.blit(surf, ((self.rectlist[i][0] + surfsize//2), (self.rectlist[i][1] + surfsize//2)))


def ai(boxes, hardness):
    #winning
    for i in range(0, 9, 3):
        if boxes[i] == boxes[i + 1] == 2 and boxes[i + 2] == False:
            return i + 2
        if boxes[i] == boxes[i + 2] == 2 and boxes[i + 1] == False:
            return i + 1
        if boxes[i + 2] == boxes[i + 1] == 2 and boxes[i] == False:
            return i
    
    for i in range(3):
        if boxes[i] == boxes[i + 3] == 2 and boxes[i + 6] == False:
            return i + 6
        if boxes[i] == boxes[i + 6] == 2 and boxes[i + 3] == False:
            return i + 3
        if boxes[i + 6] == boxes[i + 3] == 2 and boxes[i] == False:
            return i
    
    if boxes[0] == boxes[4] == 2 and boxes[8] == False:
        return 8
    if boxes[0] == boxes[8] == 2 and boxes[4] == False:
        return 4
    if boxes[4] == boxes[8] == 2 and boxes[0] == False:
        return 0

    if boxes[2] == boxes[4] == 2 and boxes[6] == False:
        return 6
    if boxes[2] == boxes[6] == 2 and boxes[4] == False:
        return 4
    if boxes[4] == boxes[6] == 2 and boxes[2] == False:
        return 2

    #preventing player from winning
    for i in range(0, 9, 3):
        if boxes[i] == boxes[i + 1] == 1 and boxes[i + 2] == False:
            return i + 2
        if boxes[i] == boxes[i + 2] == 1 and boxes[i + 1] == False:
            return i + 1
        if boxes[i + 2] == boxes[i + 1] == 1 and boxes[i] == False:
            return i
    
    for i in range(3):
        if boxes[i] == boxes[i + 3] == 1 and boxes[i + 6] == False:
            return i + 6
        if boxes[i] == boxes[i + 6] == 1 and boxes[i + 3] == False:
            return i + 3
        if boxes[i + 6] == boxes[i + 3] == 1 and boxes[i] == False:
            return i
    
    if boxes[0] == boxes[4] == 1 and boxes[8] == False:
        return 8
    if boxes[0] == boxes[8] == 1 and boxes[4] == False:
        return 4
    if boxes[4] == boxes[8] == 1 and boxes[0] == False:
        return 0
    
    if boxes[2] == boxes[4] == 1 and boxes[6] == False:
        return 6
    if boxes[2] == boxes[6] == 1 and boxes[4] == False:
        return 4
    if boxes[4] == boxes[6] == 1 and boxes[2] == False:
        return 2
    
    edge_list = []
    corner_list = []

    if boxes[4] == False:
        return 4

    for i in range(1, 8, 2):
        if boxes[i] == False:
            edge_list.append(i)
    for i in [0, 2, 6, 8]:
        if boxes[i] == False:
            corner_list.append(i)

    rand = randint(0, 99)
    rand %= 2

    print(hardness, rand)
    if (hardness == 2 and rand == 1) or hardness == 3:
        if ((boxes[1] == boxes[6] == 1) or (boxes[2] == boxes[3] == 1)) and boxes[0] == False:
            return 0
        if ((boxes[0] == boxes[5] == 1) or (boxes[1] == boxes[8] == 1)) and boxes[2] == False:
            return 2
        if ((boxes[0] == boxes[7] == 1) or (boxes[5] == boxes[8] == 1)) and boxes[6] == False:
            return 6
        if ((boxes[2] == boxes[7] == 1) or (boxes[5] == boxes[6] == 1)) and boxes[8] == False:
            return 8

    if (hardness == 2 and rand == 0) or hardness == 3:
        if (boxes[1] == boxes[3] == 1) and boxes[0] == False:
            return 0
        if (boxes[1] == boxes[5] == 1) and boxes[2] == False:
            return 2
        if (boxes[3] == boxes[7] == 1) and boxes[6] == False:
            return 6
        if (boxes[5] == boxes[7] == 1) and boxes[8] == False:
            return 8

    if boxes[4] != 1:
        if len(edge_list):
            return choice(edge_list)
        if len(corner_list):
            return choice(corner_list)
    else:
        if len(edge_list):
            return choice(corner_list)
        if len(corner_list):
            return choice(edge_list)

    
def new(grid, screen, screenCol, turn):
    for i in range(len(grid.box_used)):
        grid.box_used[i] = False
    screen.fill(screenCol)
    grid.show(screen)
    turn = 0
    return turn

def mainLoop(screenCol, textCol):
    pg.display.set_caption('Tic-Tac-Toe')
    screenWd, screenHt = 1120, 630
    screen = pg.display.set_mode((screenWd, screenHt))
    clock = pg.time.Clock()
    FPS = 25
    turn = 0
    current_mode = 1
    difficulty = 2
    won = False
    screenCenter = (screenWd//2, screenHt//2)
    grid = Grid(screenHt, 245, col = textCol)
    exit_button = Button(1050, 600, 50, 30, "Exit", textHeight = 30, textColour = textCol, opaque = False)
    new_button = Button(1000, 300, 50, 30, "New Game", textHeight = 30, textColour = textCol, opaque = False)
    butt_mode = Button(1075, 15, 20, 20)
    butt_mainMenu = Button(940, 600, 100, 30, "Main Menu", textHeight = 30, textColour = textCol, opaque = False)
    play2_butt = Button(50, 200, 150, 100, "2 player", textColour = textCol)
    play1_butt = Button(50, 400, 150, 100, "1 player", textColour = textCol)
    easy = Button(60, 550, 40, 40, 'easy', textHeight = 15, textColour = textCol, value = 1, enabled_selected = True, outline = True)
    medium = Button(110, 550, 40, 40, 'medium', textHeight = 15, textColour = textCol, value = 2, enabled_selected = True, outline = True)
    hard = Button(160, 550, 40, 40, 'hard', textHeight = 15, textColour = textCol, value = 3, enabled_selected = True, outline = True)

    diff_list = [easy, medium, hard]
    #print(grid.boxlist)
    #print(grid.rectlist)i]
    
    screen.fill(screenCol)
    grid.show(screen)

    key_check = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Quit()
                if event.key == pg.K_n:
                    turn = new(grid, screen, screenCol, turn)
                    won = False
                for i in range(len(key_check)):
                    if event.key == key_check[i] and grid.box_used[i] == False:
                        grid.mark(i, turn, screen, screenCol)
                        if turn%2 == 0:
                            grid.box_used[i] = 1
                        else:
                            grid.box_used[i] = 2
                        turn += 1


        if exit_button.get_click():
            Quit()
        if new_button.get_click():
            turn = new(grid, screen, screenCol, turn)
            won = False
        elif grid.get_click(turn, screen, screenCol):
            turn += 1
        elif butt_mode.get_click():
            if screenCol == clr.black:
                textCol = clr.black
                screenCol = clr.white
            else:
                textCol = clr.white
                screenCol = clr.black
            exit_button.textColour = textCol
            new_button.textColour = textCol
            butt_mainMenu.textColour = textCol
            grid.col = textCol
        elif butt_mainMenu.get_click():
            return screenCol, textCol
        elif play2_butt.get_click() and current_mode == 1:
            turn = new(grid, screen, screenCol, turn)
            current_mode = 2
            won = False
        elif play1_butt.get_click() and current_mode == 2:
            turn = new(grid, screen, screenCol, turn)
            current_mode = 1
            won = False

        screen.fill(screenCol)
        grid.show(screen)

        for i in range(len(grid.box_used)):
            if grid.box_used[i]:
                grid.mark(i, turn, screen, screenCol)

        if ((grid.box_used[0] == grid.box_used[1] == grid.box_used[2] == 1) or (grid.box_used[3] == grid.box_used[4] == grid.box_used[5] == 1)
            or (grid.box_used[6] == grid.box_used[7] == grid.box_used[8] == 1) or (grid.box_used[0] == grid.box_used[4] == grid.box_used[8] == 1)
            or (grid.box_used[2] == grid.box_used[4] == grid.box_used[6] == 1) or (grid.box_used[0] == grid.box_used[3] == grid.box_used[6] == 1)
            or (grid.box_used[1] == grid.box_used[4] == grid.box_used[7] == 1) or (grid.box_used[2] == grid.box_used[5] == grid.box_used[8] == 1)):
            text(screen, 0, 0, 80, 'Player 1 Wins!', textCol, screenCenter)
            won = True
            #print(won)
        if ((grid.box_used[0] == grid.box_used[1] == grid.box_used[2] == 2) or (grid.box_used[3] == grid.box_used[4] == grid.box_used[5] == 2)
            or (grid.box_used[6] == grid.box_used[7] == grid.box_used[8] == 2) or (grid.box_used[0] == grid.box_used[4] == grid.box_used[8] == 2)
            or (grid.box_used[2] == grid.box_used[4] == grid.box_used[6] == 2) or (grid.box_used[0] == grid.box_used[3] == grid.box_used[6] == 2)
            or (grid.box_used[1] == grid.box_used[4] == grid.box_used[7] == 2) or (grid.box_used[2] == grid.box_used[5] == grid.box_used[8] == 2)):
            text(screen, 0, 0, 80, 'Player 2 Wins!', textCol, screenCenter)
            won = True
            #print(won)

        text(screen, 100, 340, 20, (str(current_mode)+" Player"), textCol)

        if turn%2 == 1 and current_mode == 1 and turn <=7 and won == False:
            move = ai(grid.box_used, difficulty)
            grid.mark(move, turn, screen, screenCol)
            grid.box_used[move] = 2
            turn += 1

        if current_mode == 1:
            for diff in diff_list:
                diff.show(screen)
                if diff.value == difficulty:
                    diff.selected = True
                else:
                    diff.selected = False
                if diff.get_click():
                    turn = new(grid, screen, screenCol, turn)
                    difficulty = diff.value

        if screenCol == clr.black:
            sun(screen)
        else:
            moon(screen)
            
        if turn >= 9 and won == False:
            text(screen, 0, 0, 80, 'draw', textCol, screenCenter)
        exit_button.show(screen)
        new_button.show(screen)
        butt_mainMenu.show(screen)
        play2_butt.show(screen)
        play1_butt.show(screen)
        pg.display.update()
        clock.tick(FPS)


##try:
##    mainLoop(clr.white, clr.black)
##except:
##    traceback.print_exc()
##finally:
##    pg.quit()
    
    
