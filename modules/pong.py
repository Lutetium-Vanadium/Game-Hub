import pygame as pg
from GUI_elements import*
from clr import*
import traceback
from random import random, randrange
from math import *
from help import *

FPS = 25
clock = pg.time.Clock()
screenWd, screenHt = 1120, 630
center = (screenWd//2, screenHt//2)
Vector = pg.math.Vector2

TOT_ANGLE = 30

mode = Button(screenWd - 45, 15, 20, 20)

class Ball():
	def __init__(self, radius, col, pos, max_speed = 17, colourkey = green_screen):
		self.max_speed = max_speed
		self.velocity = self.create_velocity()
		self.surf = pg.Surface((radius*2, radius*2))
		self.surf.fill(colourkey)
		pg.draw.circle(self.surf, col, (radius, radius), radius)
		self.surf.set_colorkey(colourkey)
		self.mask = pg.mask.from_surface(self.surf)
		self.rect = pg.Rect(pos, (radius*2, radius*2))
		self.pos = pos
		self.collidingrect = pg.Rect(pos[0]+self.velocity[0], pos[1]+self.velocity[1], self.rect[2], self.rect[3])

	def move(self, screen_size):
		if self.rect[0] <= 0 or self.rect[0] >= screen_size[0]-self.rect[2]:
			return False
		
		elif self.collidingrect[1] <= 0:
			self.rect[1] = 1
			self.velocity.reflect_ip(Vector(0, 1))
		
		elif self.collidingrect[1] >= screen_size[1]-self.rect[3]:
			self.rect[1] = screen_size[1] - self.rect[3] + 1
			self.velocity.reflect_ip(Vector(0, 1))

		self.rect[0] += self.velocity.x
		self.rect[1] += self.velocity.y
		return True

	def show(self, screen):
		self.collidingrect[0] = self.rect[0] + self.velocity.x
		self.collidingrect[1] = self.rect[1] + self.velocity.y
		screen.blit(self.surf, (round(self.rect[0]), round(self.rect[1])))

	def reset(self):
		self.rect[0] = self.pos[0]
		self.rect[1] = self.pos[1]
		self.velocity = self.create_velocity()
		self.collidingrect[0] = self.pos[0] + self.velocity.x
		self.collidingrect[1] = self.pos[1] + self.velocity.y

	def create_velocity(self):
		sign = randrange(-1, 2, 2)
		direction = randrange(0, 2)
		angle = (pi*direction) + ((random() * pi / 4)  * sign) + pi/18
		vx = self.max_speed * cos(angle)
		vy = self.max_speed * sin(angle)
		return Vector(vx, vy)

class Paddle():
	def __init__(self, size, col, center, side_dist, speed = 26, colourkey = green_screen):
		self.size = size
		self.speed = speed
		x = center[0] - size[0]//2
		y = center[1] - size[1]//2
		self.pos = [x, y]
		self.surf = pg.Surface(size)
		self.surf.fill(colourkey)
		r = size[0]//2
		pg.draw.rect(self.surf, col, (0, r, size[0], size[1]-r-r))
		pg.draw.circle(self.surf, col, (r, r), r)
		pg.draw.circle(self.surf, col, (r, size[1]-r), r)
		self.surf.set_colorkey(green_screen)
		size = list(size)
		size[0] += 2 * side_dist
		self.rect = pg.Rect((x-side_dist, y), size)

	def move(self, sign, screen_size):
		self.pos[1] += sign * self.speed
		if self.pos[1] <= 5:
			self.pos[1] = 5
		elif self.pos[1] >= screen_size[1]-5-self.size[1]:
			self.pos[1] = screen_size[1] - 5 -self.size[1]
		self.rect[1] = self.pos[1]

	def show(self, screen):
		screen.blit(self.surf, self.pos)

	def hit(self, ball):
		return self.rect.colliderect(ball.collidingrect)

	def map_to_vector(self, val, velocity):
		ratio = val / self.size[1]
		angle = (ratio * TOT_ANGLE) - TOT_ANGLE/2
		normal = Vector(tan(radians(angle)), 1)
		velocity.rotate_ip(180)
		velocity.reflect_ip(normal);

class Field():
	def __init__(self, paddle_size = (6, 110), paddle_dist = 10, pos = (10, 10), size = (1100, 500),
				 dark_col = dark_dark_gray, light_col = light_gray, paddle_col = gray, ball_col = red):
		self.size = size
		self.pos = pos
		self.dark_col = dark_col
		self.light_col = light_col
		self.paddle_pos = ([ paddle_dist ,  size[1]//2 - paddle_size[1]//2] ,
						 [ size[0] - (paddle_dist + paddle_size[0]) ,  size[1]//2 - paddle_size[1]//2] )
		
		self.paddle1 = Paddle(paddle_size, paddle_col, self.paddle_pos[0], paddle_dist)
		self.paddle2 = Paddle(paddle_size, paddle_col, self.paddle_pos[1], paddle_dist)
		self.ball = Ball(6, ball_col, (size[0]//2, size[1]//2))
		self.ball_properties = (6, ball_col, (size[0]//2, size[1]//2))
		self.surf = pg.Surface(size)
		self.obj_list = [self.paddle1, self.paddle2, self.ball]
		self.play = True

	def show(self, screen, dark_mode, paused, game_over):
		moved = False
		if dark_mode:
			self.surf.fill(self.dark_col)
		else:
			self.surf.fill(self.light_col)
		for obj in self.obj_list:
			obj.show(self.surf)
		if self.paddle1.hit(self.ball):
			x = self.paddle1.pos[0] + self.paddle1.size[0]
			diff = (x - self.ball.rect[0])/self.ball.velocity[0]

			self.ball.rect[1] += (self.ball.velocity[1] * diff)
			self.ball.rect[0] = x

			y = self.ball.rect[1] - self.paddle1.rect[1]
			self.paddle1.map_to_vector(y, self.ball.velocity)

			moved = True
		
		elif self.paddle2.hit(self.ball):
			x = self.paddle2.pos[0] - self.ball.rect[2]
			diff = (x - self.ball.rect[0])/self.ball.velocity[0]
			
			self.ball.rect[1] += (self.ball.velocity[1] * diff)
			self.ball.rect[0] = x
			
			y = self.ball.rect[1] - self.paddle2.rect[1]
			self.paddle2.map_to_vector(y, self.ball.velocity)

			moved = True
		
		if paused == game_over == moved == False and self.play:
			self.play = self.ball.move(self.size)

		screen.blit(self.surf, self.pos)
		
		if self.play == paused == False:
			if self.ball.rect[0] > self.size[0]//2:
				return 1
			else:
				return 2
		return None
	def reset(self):
		self.ball.reset()
		self.paddle1.pos = self.paddle_pos[0]
		self.paddle1.rect[1] = self.paddle1.pos[1]
		self.paddle2.pos = self.paddle_pos[1]
		self.paddle2.rect[1] = self.paddle2.pos[1]
		self.play = True

def mode_change(dark_mode):
	if dark_mode:
		return white, black, False
	else:
		return black, white, True

def mainLoop(screencol, textcol, prev_screen = None, rect_pos = None, start = False):
	pg.display.set_caption("Pong")
	screen = pg.display.set_mode((screenWd, screenHt))
	if screencol == black:
		dark_mode = True
	else:
		dark_mode = False
	paused =False
	score = [0,0]
	game_over = False
	games = 3
	new = Button(center[0] - 230, 520, 200, 80, "New Game", textHeight = 30, textColour = textcol, opaque = False)
	home = Button(center[0] + 30, 520, 200, 80, "Home", textHeight = 30, textColour = textcol, opaque = False)

	button_list = [new, home]

	field = Field()

	while score[0] <= games and score[1] <= games:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				Quit(screen)
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					fade(screen, True, col = screencol)
					return False, screencol, textcol
				elif event.key == pg.K_h:
					if start == False:
						paused = True
					fade(screen, True, col = screencol)
					help_screen(PONG, screencol, textcol)
				elif event.key == pg.K_m:
					screencol, textcol, dark_mode = mode_change(dark_mode)
					for button in button_list:
						button.textColour = textcol
				elif event.key == pg.K_p and game_over == False:
					if paused:
						paused = False
					else:
						paused = True
				elif event.key == pg.K_n:
					return True, screencol, textcol
				elif event.key == pg.K_r:
					field.play = False
					paused = True

		if paused == False:

			keystate = pg.key.get_pressed()

			if keystate[pg.K_UP]:
				field.paddle2.move(-1, field.size)
			if keystate[pg.K_DOWN]:
				field.paddle2.move(1, field.size)
			if keystate[pg.K_w]:
				field.paddle1.move(-1, field.size)
			if keystate[pg.K_s]:
				field.paddle1.move(1, field.size)

		screen.fill(screencol)

		if mode.get_click():
			screencol, textcol, dark_mode = mode_change(dark_mode)
			for button in button_list:
				button.textColour = textcol
		elif new.get_click():
			return True, screencol, textcol
		elif home.get_click():
			fade(screen, True, col = screencol)
			return False, screencol, textcol

		win = field.show(screen, dark_mode, paused, game_over)
		if win != None:
			score[win-1] += 1
			if score[0] == games:
				win_text = "Player 1 Wins!"
				game_over = True
			if score[1] == games:
				win_text = "Player 2 Wins!"
				game_over = True

		if screencol == black:
			sun(screen)
		else:
			moon(screen)

		if paused and field.play:
			text(screen, 0, 0, 50, "Paused", textcol, center)
		elif game_over:
			text(screen, 0, 0, 50, win_text, textcol, center)

		center_y = (screenHt  + field.size[1] + field.pos[1])//2
		center_change = (screenHt - field.size[1] - field.pos[1])//8
		# center_change = 0
		size = (screenHt - field.size[1] - field.pos[1])//4

		text(screen, 0, 0, size, "Player 1:", textcol, (screenWd//8, center_y-center_change))
		text(screen, 0, 0, size, str(score[0]), textcol, (screenWd//8, center_y+center_change))
		text(screen, 0, 0, size, "Player 2:", textcol, (7*screenWd//8, center_y-center_change))
		text(screen, 0, 0, size, str(score[1]), textcol, (7*screenWd//8, center_y+center_change))
		
		for button in button_list:
			button.show(screen)

		if start:
			expand(screen, screen.copy(), [rect_pos[0], rect_pos[1]+43, 200, 113], prev_screen)
			start = False
		else:
			pg.display.update()

		if field.play == False:
			pg.time.wait(500)
			field.reset()
			paused = False
		clock.tick(FPS)

# try:
# 	replay = True
# 	screencol, textcol = black, white
# 	while replay:
# 		replay, screencol, textcol = mainLoop(screencol, textcol)
# except:
# 	traceback.print_exc()
# finally:
# 	pg.quit()