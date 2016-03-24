import pygame
from pygame.locals import *
import math
import time

START = 320, 240
ENDX = range(0, 641)
ENDY = range(0, 481)
WINDOW_SIZE = 640, 480

def main():
	pygame.init()
	
	screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
	pygame.display.set_caption("fire")
	screen.fill((255, 0, 0))
	
	doro = pygame.image.load("doro.png").convert()
	colorkey = doro.get_at((0, 0))
	doro.set_colorkey(colorkey, RLEACCEL)
	doro_rect = doro.get_rect()
	doro_rect.center = (160, 120)
	
	while True:
		
		for i in ENDX:
			for j in ENDY:
				for k in range(1, 101):
					screen.blit(doro, doro_rect)
					pygame.display.update()
					doro_rect.move_ip((i / 100) * k, (j / 100) * k)
					time.sleep(0.1)
					
if __name__ == "__main__":
	main()