import pygame as pg
from GUI_elements import*
from clr import*
import traceback
from random import randint
from help import*

screenWd, screenHt = 1120, 630
screenCenter = (screenWd//2, screenHt//2)
clock = pg.time.Clock()
BOMB = -1
FPS = 15
LEFT = 0
RIGHT = 2
SETTINGS = None
WIDTH = 1
HEIGHT = 2

class Box():
	def __init__(self, wd, surfpos, x = 0, y = 0, textcol = black, txt = '', outline = True, activated = True, value = None,
				 dark_col = [gray, dark_gray, dark_dark_gray], light_col = [light_light_gray, light_gray, gray]):
		self.surfpos = surfpos
		self.surf = pg.Surface((wd, wd))
		self.rect = self.surf.get_rect()
		self.rect[0] = x
		self.rect[1] = y
		self.text = text
		self.textcol = textcol
		self.dark_col = dark_col
		self.light_col = light_col
		self.activated = activated
		self.wd = wd
		self.val = value
		self.pos = (x, y)
		self.outline = outline
		self.txt = txt
		self.flagged = False
		self.clicked = False
	def onButton(self):
		mpos = list(pg.mouse.get_pos())
		mpos[0] -= self.surfpos[0]
		mpos[1] -= self.surfpos[1]
		return self.rect.collidepoint(mpos)
	def show(self, screen, textcol, thickness = 2):
		if textcol == black:
			col_list = self.light_col
		else:
			col_list = self.dark_col
		self.surf.fill(col_list[1])
		if self.outline:
			pg.draw.line(self.surf, textcol, (0,0), (self.wd,0), thickness)
			pg.draw.line(self.surf, textcol, (self.wd,self.wd), (self.wd,0), thickness)
			pg.draw.line(self.surf, textcol, (0,self.wd), (self.wd,self.wd), thickness)
			pg.draw.line(self.surf, textcol, (0,self.wd), (0,0), thickness)
		wd = 3 * self.wd//5
		if self.val != BOMB:
			text(self.surf, 0, 0, wd, self.txt, textcol, (self.wd//2, self.wd//2))
		else:
			pos = (self.wd//3, self.wd//3)
			sun(self.surf, red, pos, pos)
		if self.activated:
			pg.draw.polygon(self.surf, col_list[0], [(0,self.wd), (0,0), (self.wd, 0)])
			pg.draw.polygon(self.surf, col_list[2], [(self.wd, 0), (self.wd, self.wd), (0,self.wd)])
			pg.draw.rect(self.surf, col_list[1], (wd//3, wd//3, wd, wd))
		if self.flagged:
			pg.draw.line(self.surf, textcol, (self.wd//2, self.wd//5), (self.wd//2, 4*self.wd//5), thickness)
			pg.draw.polygon(self.surf, red, [(self.wd//2, self.wd//5), (3*self.wd//4, 3*self.wd//10), (self.wd//2, 2*self.wd//5)])
		screen.blit(self.surf, self.pos)
	def click(self, button, count = None):
		temp = bool((self.onButton() and pg.mouse.get_pressed()[button]))
		if self.clicked == False and temp:
			self.clicked = True
			return temp
		if self.clicked and temp == False:
			self.clicked = False
		return False

class Grid():
	def __init__(self, size, n_bombs, textcol):
		self.size = size
		self.blocksize = screenHt//size[1]
		self.wd = size[0] * self.blocksize
		self.ht = size[1] * self.blocksize
		self.loc = ((screenWd - (size[0] * self.blocksize) + 100)//2, 0)
		self.box_list = [[Box(self.blocksize, self.loc, self.blocksize*i, self.blocksize*j, textcol)
						 for j in range(size[1])] for i in range(size[0])]
		
		while n_bombs > 0:
			rand_i = randint(0, self.size[0]-1)
			rand_j = randint(0, self.size[1]-1)
			if self.box_list[rand_i][rand_j].val != BOMB:
				self.box_list[rand_i][rand_j].val = BOMB
				self.box_list[rand_i][rand_j].txt = 'b'
				n_bombs -= 1
		self.surf = pg.Surface((self.wd, self.ht))
		self.pressed = [False, False]
		self.alive = True
		self.score = 0
		self.flags = 0
		for i in range(size[0]):
			for j in range(size[1]):
				if self.box_list[i][j].val != BOMB:
					c = 0
					if (i < size[0]-1) and (j < size[1]-1) and self.box_list[i+1][j+1].val == BOMB:
						c += 1
					if (i < size[0]-1) and j > 0 and self.box_list[i+1][j-1].val == BOMB:
						c += 1
					if i > 0 and (j < size[1]-1) and self.box_list[i-1][j+1].val == BOMB:
						c += 1
					if i > 0 and j > 0 and self.box_list[i-1][j-1].val == BOMB:
						c += 1
					if (i < size[0]-1) and self.box_list[i+1][j].val == BOMB:
						c += 1
					if (j < size[1]-1) and self.box_list[i][j+1].val == BOMB:
						c += 1
					if i > 0 and self.box_list[i-1][j].val == BOMB:
						c += 1
					if j > 0 and self.box_list[i][j-1].val == BOMB:
						c += 1
					self.box_list[i][j].txt = str(c)
					self.box_list[i][j].val = c

	def expand(self, i, j):
		queue  = [(i,j)]
		self.box_list[i][j].txt = ''
		check = False
		while len(queue) > 0:
			x, y = queue.pop(0)
			if self.box_list[x][y].txt == '' and check:
				continue
			
			if x > 0:
				self.box_list[x-1][y].activated = False
				if self.box_list[x-1][y].val == 0:
					queue.append((x-1, y))
			
			if y > 0:
				self.box_list[x][y-1].activated = False
				if self.box_list[x][y-1].val == 0:
					queue.append((x, y-1))
			
			if x < self.size[0]-1:
				self.box_list[x+1][y].activated = False
				if self.box_list[x+1][y].val == 0:
					queue.append((x+1, y))
			
			if y < self.size[1]-1:
				self.box_list[x][y+1].activated = False
				if self.box_list[x][y+1].val == 0:
					queue.append((x, y+1))
			
			if (x < self.size[0]-1) and (y < self.size[1]-1):
				self.box_list[x+1][y+1].activated = False
				if self.box_list[x+1][y+1].val == 0:
					queue.append((x+1, y+1))
			
			if (x < self.size[0]-1) and y > 0:
				self.box_list[x+1][y-1].activated = False
				if self.box_list[x+1][y-1].val == 0:
					queue.append((x+1, y-1))
			
			if x > 0 and (y < self.size[1]-1):
				self.box_list[x-1][y+1].activated = False
				if self.box_list[x-1][y+1].val == 0:
					queue.append((x-1, y+1))
			
			if x > 0 and y > 0:
				self.box_list[x-1][y-1].activated = False
				if self.box_list[x-1][y-1].val == 0:
					queue.append((x-1, y-1))
			self.box_list[x][y].txt = ''
			check = True
	def click(self, i, j, screen):
		box = self.box_list[i][j]
		if box.flagged or box.activated == False:
			return
		box.activated = False
		self.pressed[0] = True
		if box.val == BOMB:
			self.alive = False
		elif box.val == 0:
			i = box.pos[0]//self.blocksize
			j = box.pos[1]//self.blocksize
			self.expand(i, j)
		self.score += 1
	def show(self, screen, textcol, count):
		self.surf.fill(white)
		score = 0

		for lst in self.box_list:
			for box in lst:
				box.show(self.surf, textcol)
				if box.activated == False or box.flagged:
					score += 1
				if self.alive:
					if box.click(LEFT) and self.pressed[0] == False and box.flagged == False:
						i = box.pos[0]//self.blocksize
						j = box.pos[1]//self.blocksize
						if box.activated == False:
							if (i < self.size[0]-1) and (j < self.size[1]-1):
								self.click(i+1, j+1, screen)
							if (i < self.size[0]-1) and j > 0:
								self.click(i+1, j-1, screen)
							if i > 0 and (j < self.size[1]-1):
								self.click(i-1, j+1, screen)
							if i > 0 and j > 0:
								self.click(i-1, j-1, screen)
							if (i < self.size[0]-1):
								self.click(i+1, j, screen)
							if (j < self.size[1]-1):
								self.click(i, j+1, screen)
							if i > 0:
								self.click(i-1, j, screen)
							if j > 0:
								self.click(i, j-1, screen)
						box.activated = False
						self.pressed[0] = True
						if box.val == BOMB and box.flagged == False:
							self.alive = False
						elif box.val == 0:
							self.expand(i, j)
						self.score += 1
					elif box.click(RIGHT) and self.pressed[1] == False and box.activated:
						if box.flagged:
							box.flagged = False
							self.flags -= 1
						else:
							box.flagged = True
							self.flags += 1
						self.pressed[1] = True
				else:
					box.activated = False
		if self.pressed[0] and pg.mouse.get_pressed()[LEFT] == False:
			self.pressed[0] = False
		if self.pressed[1] and pg.mouse.get_pressed()[RIGHT] == False:
			self.pressed[1] = False

		# self.box_list[0][0].show(self.surf, textcol)
		self.score = score

		screen.blit(self.surf, self.loc)

def settings(screencol, textcol, size, n_bombs):
	size_x = 380
	pg.display.set_caption("Minesweeper - Settings")
	screen = pg.display.set_mode((screenWd, screenHt))
	editing = False
	error = False
	diff = 1
	start = True
	txt = Text(size_x, 550, 50, (500, 100), '', textcol, center = True)

	exit = Button(1050, 600, 50, 30, "Exit", textHeight = 30, textColour = textcol, opaque = False)
	mode = Button(1075, 15, 20, 20)
	back = Button(950, 600, 50, 30, "Back", textHeight = 30, textColour = textcol, opaque = False)
	width = Button(size_x, 100, 500, 200, "Width: " + str(size[0]), textColour = textcol, value = size[0])
	height = Button(size_x, 350, 500, 200, "Height: " + str(size[1]), textColour = textcol, value = size[1])

	easy = Button(125, 225, 50, 50, "Easy", textHeight = 20, textColour = textcol, value = 1,
				  enabled_selected = True, outline = True)
	medm = Button(125, 325, 50, 50, "Medium", textHeight = 20, textColour = textcol, value = 2,
				  enabled_selected = True, outline = True)
	hard = Button(125, 425, 50, 50, "Hard", textHeight = 20, textColour = textcol, value = 3,
				  enabled_selected = True, outline = True)

	diff = round(2*(n_bombs - 5)/(width.value+height.value))

	nums = {pg.K_1:'1', pg.K_2:'2', pg.K_3:'3', pg.K_4:'4', pg.K_5:'5', pg.K_6:'6', pg.K_7:'7', pg.K_8:'8', pg.K_9:'9', pg.K_0:'0'}

	b_list = [exit, back, width, height, easy, medm, hard]
	transparent_object_list = [exit, back, txt]
	bomb_b_list = [easy, medm, hard]
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				Quit(screen)
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					n_bombs = diff * (width.value + height.value)//2 + 5
					fade(screen, True, col = screencol)
					return (width.value, height.value), n_bombs, screencol, textcol
				if event.key in nums and txt.cursor:
					txt.text += nums[event.key]
				elif event.key == pg.K_BACKSPACE:
					txt.text = txt.text[:-1]
				elif event.key == pg.K_RETURN and editing != False:
					s = txt.text
					if editing == WIDTH:
						width.text = "Width: " + s
						width.value = int(s)
					else:
						height.text = "Height: " + s
						height.value = int(s)
					txt.location = [size_x, 550]
					txt.cursor = False
					txt.text = ''
					editing = False
				elif event.key == pg.K_h:
					fade(screen, True, col = screencol)
					help_screen(MINESWEEPER, screencol, textcol)
				elif event.key == pg.K_m:
					if screencol == clr.black:
						screencol = clr.white
						textcol = clr.black
					else:
						screencol = clr.black
						textcol = clr.white
					for obj in transparent_object_list:
						obj.textColour = textcol
		
		screen.fill(screencol)

		if exit.get_click():
			Quit(screen)
		elif mode.get_click():
			if screencol == clr.black:
				screencol = clr.white
				textcol = clr.black
			else:
				screencol = clr.black
				textcol = clr.white
			for obj in transparent_object_list:
				obj.textColour = textcol
		elif back.get_click():
			n_bombs = diff * (width.value + height.value)//2 + 5
			fade(screen, True, col = screencol)
			return (width.value, height.value), n_bombs, screencol, textcol
		elif width.get_click():
			txt.location = [size_x, 250]
			i = 0
			editing = WIDTH
			txt.text = str(width.value)
			txt.cursor = True
			txt.size = 50
			error = False
		elif height.get_click():
			txt.location = [size_x, 450]
			i = 1
			editing = HEIGHT
			txt.text = str(height.value)
			txt.cursor = True
			txt.size = 50
			error = False
		for button in bomb_b_list:
			if button.get_click():
				diff = button.value
			if button.value != diff:
				button.selected = False
			else:
				button.selected = True

		if width.value > int(4/3 * height.value):
			max_width = int(4/3 * height.value)
			width.value = max_width
			width.text = "Width: " + str(max_width)
			error = True

		if screencol == clr.black:
			sun(screen)
		else:
			moon(screen)

		for button in b_list:
			button.show(screen)

		if error:
			text(screen, 0, 0, 30, "Error: Aspect ratio is unacceptable", red, (size_x + 250, 590))

		text(screen, 0, 0, 30, "Choose a width and height such that they are at the widest a 4:3 ratio", textcol, (size_x+250, 50))
		text(screen, 0, 0, 40, "Bombs:", textcol, (180, 100))

		txt.display(screen)
		
		if start:
			fade(screen, False)
			start = False
		else:
			pg.display.update()
		clock.tick(FPS)

def mainLoop(screencol, textcol, size, n_bombs, prev_screen = None, rect_pos = None, back = True):
	pg.display.set_caption("Minesweeper")
	screen = pg.display.set_mode((screenWd, screenHt))
	count = 0
	time = 0
	start = True

	grid = Grid(size, n_bombs, textcol)

	butt_mode = Button(1075, 15, 20, 20)
	butt_new = Button(25, 200, 140, 50, 'new game', textHeight = 30, colour = light_gray, hovourColour = light_light_gray, outline = True)
	butt_home = Button(25, 275, 140, 50, 'home', textHeight = 30, colour = light_gray, hovourColour = light_light_gray, outline = True)
	settings = Button(25, 550, 140, 50, 'Settings', textHeight = 30, colour = light_gray, hovourColour = light_light_gray, outline = True)
	exit = Button(1050, 600, 50, 30, "Exit", textHeight = 30, textColour = textcol, opaque = False)

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				Quit(screen)
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					fade(screen, True, col = screencol)
					return False, screencol, textcol
				if event.key == pg.K_n:
					return True, screencol, textcol
				elif event.key == pg.K_h:
					fade(screen, True, col = screencol)
					help_screen(MINESWEEPER, screencol, textcol)
				elif event.key == pg.K_m:
					if screencol == clr.black:
						screencol = clr.white
						textcol = clr.black
					else:
						screencol = clr.black
						textcol = clr.white
					exit.textColour = textcol

		if butt_mode.get_click():
			if screencol == clr.black:
				screencol = clr.white
				textcol = clr.black
			else:
				screencol = clr.black
				textcol = clr.white
			exit.textColour = textcol
		elif butt_new.get_click():
			return True, screencol, textcol
		elif butt_home.get_click():
			fade(screen, True, col = screencol)
			return False, screencol, textcol
		elif settings.get_click():
			return SETTINGS, screencol, textcol
		elif exit.get_click():
			Quit(screen)

		if grid.alive == False:
			col = red
		elif grid.score == grid.size[0] * grid.size[1]:
			col = select_green
		else:
			col = screencol

		screen.fill(col)

		grid.show(screen, textcol, count)

		if screencol == clr.black:
			sun(screen)
		else:
			moon(screen)

		text(screen, 20, 20, 30, "Time: " + str(time), textcol)
		text(screen, 20, 70, 40, "Score: " + str(grid.score), textcol)
		text(screen, 20, 120, 30, "Bombs left: " + str(n_bombs - grid.flags), textcol)
		butt_home.show(screen)
		butt_new.show(screen)
		settings.show(screen)
		exit.show(screen)

		if back:
			fade(screen, False)
			back = False
		elif start and prev_screen != None:
			expand(screen, screen.copy(), [rect_pos[0], rect_pos[1]+150, 200, 113], prev_screen)
			start = False
		else:
			pg.display.update()

		count += 1

		if count % FPS == 0 and grid.alive:
			time += 1
		
		clock.tick(FPS)

# try:
# 	size, n_bombs = (12, 9), 10
# 	screencol, textcol = black, white
# 	replay = True
# 	while replay:
# 		replay, screencol, textcol = mainLoop(screencol, textcol, size, n_bombs)
# 		if replay == SETTINGS:
# 			size, n_bombs, screencol, textcol = settings(screencol, textcol, size, n_bombs)
# 			replay = True
# except:
# 	traceback.print_exc()
# finally:
# 	pg.quit()
