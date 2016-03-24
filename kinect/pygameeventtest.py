import cv2
import sys
import numpy as np
import kinectskeleton as ks
import pygame
from pygame.locals import *
from pykinect import nui

KINECTVIDEO = pygame.USEREVENT
WINDOW_SIZE = 640, 480

def numpyToSurface(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = pygame.surfarray.make_surface(img)
	img = pygame.transform.rotate(img, -90)
#	img = pygame.transform.flip(img, True, False)
	return img

def video_frame_ready(frame):
	try:
		video = np.empty((480, 640, 4), np.uint8)
		frame.image.copy_bits(video.ctypes.data)
		video = numpyToSurface(video)
		pygame.event.post(pygame.event.Event(KINECTVIDEO, video_frame = video))
	except:
		pass

def main():
	pygame.init()
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("video")
	with nui.Runtime() as kinect:
	
		kinect.video_frame_ready += video_frame_ready
		kinect.skeleton_engine.enabled = True
		kinect.skeleton_frame_ready += ks.post_frame
		kinect.video_stream.open(nui.ImageStreamType.video, 2,
							nui.ImageResolution.Resolution640x480, 
							nui.ImageType.Color)
							
		while True:
			e = pygame.event.wait()
			if e.type == QUIT:
				break
				
			elif e.type == KEYDOWN:
				if e.key == K_q:
					break
				
			elif e.type == KINECTVIDEO:
				screen.blit(e.video_frame, (0, 0))
				pygame.display.update()
				
if __name__ == "__main__":
	main()