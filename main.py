import pygame
from random import randint

class Player:
	def __init__(self):
		self.direction = 1
	
	def draw(self, surf):
		if self.direction:
			pygame.draw.rect(surf, (0, 0, 0), (80, 256 - 20, 10, 20))
		else:
			pygame.draw.rect(surf, (255, 255, 255), (80, 256, 10, 20))

class Obstacle:
	def __init__(self, direction):
		self.direction = direction
		
		self.x = 288
			
	def draw(self, surf):
		if self.direction:
			pygame.draw.rect(surf, (0, 0, 0), (self.x, 256 - 20, 10, 20))
		else:
			pygame.draw.rect(surf, (255, 255, 255), (self.x, 256, 10, 20))
	
	def move(self, speed):
			self.x -= speed

class Star:
	def __init__(self, scale, pos):
			self.image = pygame.transform.scale(pygame.image.load('e' + str(scale) + '.png'), (10, 10))
			self.x, self.y = pos
			self.scale = scale
			
	def draw(self, surf):
			surf.blit(self.image, (self.x, self.y))
		
	def move(self, speed ):
			self.x -= self.scale * speed / 3

class Cloud:
	def __init__(self, y):
		self.image = pygame.transform.scale(pygame.image.load('cloud.png'), (32, 32))
		
		self.x, self.y = (288, y)
	
	def draw(self, surf):
		surf.blit(self.image, (self.x, self.y))
		
	def move(self, speed):
		self.x -= 2
		
		
def draw(screen):
	screen.fill((255,255,255))
	pygame.draw.rect(screen, (0,0,0), (0, 256, 288, 256))
	p.draw(screen)
	screen.blit(sun, (sunpos[0], sunpos[1]))
	screen.blit(moon, (moonpos[0], moonpos[1]))
	for o in obstacles:
		o.draw(screen)
	for s in stars:
		s.draw(screen)
	for c in clouds:
		c.draw(screen)
	screen.blit(text, (10, 10))
	pygame.display.update()

pygame.init()

FPS = 60
SCREENWIDTH = 288
SCREENHEIGHT = 512

screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT), pygame.SCALED ) #| pygame.FULLSCREEN
clock = pygame.time.Clock()

speed = 2
oframe = 0
sframe = 0
cframe = 0

p = Player()
obstacles = []
stars = []
clouds = []

sun = pygame.transform.scale(pygame.image.load('sun.png'), (32,32))
moon = pygame.transform.scale(pygame.image.load('moon.png'),(32,32))
sunpos = [238,20]
moonpos = [30,462]

score = 0

pygame.font.init()
font = pygame.font.SysFont('freesansbold.ttf', 20)
text = font.render('0', True, (0,0,0))

while True:
	oframe += 1
	sframe += 1
	cframe += 1
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if p.direction:
				p.direction = 0
			else:
				p.direction = 1
	
	for i,o in enumerate(obstacles):
		o.move(speed)
		if o.x < 80 < o.x + 10:
			if p.direction == o.direction:
				exit()
		elif o.x < 0:
			score += 1
			obstacles.pop(i)
	
	for i, s in enumerate(stars):
		s.move(speed)
		if s.x < 0:
			stars.pop(i)
			
	for i, c in enumerate(clouds):
		c.move(speed)
		if c.x < -32:
			clouds.pop(i)
	
	if oframe > 40:
		oframe = 0
		obstacles.append(Obstacle(randint(0, 1)))
		
	if sframe > 10:
		sframe = 0
		stars.append(Star(randint(1,3), (288, randint(280, 512))))
	
	if cframe > randint(1,3) * 40:
		cframe = 0
		clouds.append(Cloud(randint(50, 150)))
	
	draw(screen)
	
	moonpos[0] -= speed / 3
	sunpos[0] -= speed / 3
	
	if moonpos[0] < -20:
		moonpos[0] = 288
		
	if sunpos[0] < -20:
		sunpos[0] = 288
		
	speed += 0.001
 	
	text = font.render("Score : " + str(score), True, (0,0,0))
	