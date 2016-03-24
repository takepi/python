import pygame
from pygame.locals import*
import sys
from pygame import QUIT

def main():
    pygame.init

    screen = pygame.display.set_mode((300,400))
    pygame.display.set_caption("test")

    while True:
        screen.fill((0,0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__=="__main__":
    main()