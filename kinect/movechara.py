import pygame
from pygame.locals import *

WINDOW_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("dango")

dango = pygame.image.load("dango.png").convert()
colorkey = dango.get_at((0, 0))
dango.set_colorkey(colorkey, RLEACCEL)
dango_rect = dango.get_rect()
dango_rect.center = (320, 240)

vx = vy = 10

while True:
	screen.fill((255, 150, 0))
	screen.blit(dango, dango_rect)
	pygame.display.update()
	
	print dango_rect.center
	
	e = pygame.event.wait()
	if e.type == QUIT:
		break
	if e.type == KEYDOWN:
		if e.key == K_LEFT:
			dango_rect.move_ip(-vx, 0)
		elif e.key == K_RIGHT:
			dango_rect.move_ip(vx, 0)
		elif e.key == K_UP:
			dango_rect.move_ip(0, -vy)
		elif e.key == K_DOWN:
			dango_rect.move_ip(0, vy)