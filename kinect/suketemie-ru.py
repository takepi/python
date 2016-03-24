import cv2
import sys
import numpy as np
import pygame
from pygame.locals import *
from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters
from pygame.color import THECOLORS
import kinectskeleton as ks

KINECTEVENT = pygame.USEREVENT
WINDOW_SIZE = 640, 480

SKELETON_COLORS = [THECOLORS["red"], 
				   THECOLORS["blue"], 
				   THECOLORS["green"], 
				   THECOLORS["orange"],
				   THECOLORS["purple"], 
				   THECOLORS["yellow"], 
				   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
			JointId.ShoulderLeft,
			JointId.ElbowLeft, 
			JointId.WristLeft, 
			JointId.HandLeft)
			
RIGHT_ARM = (JointId.ShoulderCenter, 
			 JointId.ShoulderRight, 
			 JointId.ElbowRight, 
			 JointId.WristRight, 
			 JointId.HandRight)
			 
LEFT_LEG = (JointId.HipCenter, 
			JointId.HipLeft, 
			JointId.KneeLeft, 
			JointId.AnkleLeft, 
			JointId.FootLeft)
			
RIGHT_LEG = (JointId.HipCenter, 
			 JointId.HipRight, 
			 JointId.KneeRight, 
			 JointId.AnkleRight, 
			 JointId.FootRight)
			 
SPINE = (JointId.HipCenter, 
		 JointId.Spine, 
		 JointId.ShoulderCenter, 
		 JointId.Head)
		 
skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def numpyToSurface(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = pygame.surfarray.make_surface(img)
	img = pygame.transform.rotate(img, -90)
#	img = pygame.transform.flip(img, True, False)
	return img
	
pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
pygame.display.set_caption("Skeleton")
screen.fill(pygame.color.THECOLORS["black"])

def video_frame_ready(frame):
	video = np.empty((480, 640, 4), np.uint8)
	frame.image.copy_bits(video.ctypes.data)
	video = numpyToSurface(video)
	screen.blit(video, (0, 0))

with nui.Runtime() as kinect:

	kinect.skeleton_engine.enabled = True
	kinect.skeleton_frame_ready += ks.post_frame
	kinect.video_frame_ready += video_frame_ready

	kinect.video_stream.open(nui.ImageStreamType.video, 2, 
						nui.ImageResolution.Resolution640x480, 
						nui.ImageType.Color)

	while True:
		pygame.display.update()
		e = pygame.event.wait()
		if e.type == pygame.QUIT:
			break
		elif e.type == KINECTEVENT:
			ks.draw_skeletons(pygame.display.Info(), video, e.skeleton_frame.SkeletonData)
			pass
		elif e.type == KEYDOWN:
			if e.key == K_q:
				break
				