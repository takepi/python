import numpy as np 
import pygame
import cv2
import time

pygame.init()
type = pygame.surfarray.get_arraytypes()
pygame.surfarray.use_arraytype(type[0])

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("aaa")

hana = cv2.imread("hana.jpg", 1)

hana_s = cv2.cvtColor(hana, cv2.COLOR_BGR2RGB)
hana_img = pygame.surfarray.make_surface(hana_s)
hana_img = pygame.transform.rotate(hana_img, -90)
hana_img = pygame.transform.flip(hana_img, True, False)

screen.blit(hana_img, (0, 0))
cv2.imshow("hana", hana)

pygame.display.update()

while True:
	if cv2.waitKey(10) == 27:
		break