import cv2
import sys
import numpy as np
import pygame
from pygame.locals import  *
from pykinect import nui
	
def numpyToSurface(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = pygame.surfarray.make_surface(img)
	img = pygame.transform.rotate(img, -90)
#	img = pygame.transform.flip(img, True, False)
	return img
	
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("aaa")
kinect = nui.Runtime()

def video_frame_ready(frame):
	video = np.empty((480, 640, 4), np.uint8)
	frame.image.copy_bits(video.ctypes.data)
	video = numpyToSurface(video)
	screen.blit(video, (0, 0))

kinect.video_frame_ready += video_frame_ready

kinect.video_stream.open(nui.ImageStreamType.video, 2, 
					nui.ImageResolution.Resolution640x480, 
					nui.ImageType.Color)
					
while True:
	pygame.display.update()

	for e in pygame.event.get():
		if e.type == QUIT:
			kinect.close()
			sys.exit()
		if e.type == KEYDOWN:
			if e.key == K_q:
				kinect.close()
				sys.exit()