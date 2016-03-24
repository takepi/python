from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters
from pygame.color import THECOLORS

import pygame
from pygame.locals import *
import time
import itertools

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

def post_frame(frame):
	try:
		pygame.event.post(pygame.event.Event(KINECTEVENT, skeleton_frame = frame))
	except:
		pass
		
def draw_skeleton_data(dispInfo, screen, pSkelton, index, positions, width = 4):
	start = pSkelton.SkeletonPositions[positions[0]]
	
	for position in itertools.islice(positions, 1, None):
		next = pSkelton.SkeletonPositions[position.value]
		
		curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h)
		curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)
		
		pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
		start = next
		
def draw_skeletons(dispInfo, screen, skeletons):
	screen.fill(pygame.color.THECOLORS["black"])
	
	for index, skeleton_info in enumerate(skeletons):
		if skeleton_info.eTrackingState == SkeletonTrackingState.TRACKED:
			HeadPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h)
			
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, SPINE, 10)
			pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 10, 0)
			
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_ARM)
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_ARM)
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_LEG)
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_LEG)
		
def main():
	pygame.init()
	
	screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
	pygame.display.set_caption("Skeleton")
	screen.fill(pygame.color.THECOLORS["black"])
	
	with nui.Runtime() as kinect:
		kinect.skeleton_engine.enabled = True
		kinect.skeleton_frame_ready += post_frame
	
		while True:
			e = pygame.event.wait()
			if e.type == pygame.QUIT:
				break
				
			elif e.type == KEYDOWN:
				if e.key == K_q:
					break
				
			elif e.type == KINECTEVENT:
				draw_skeletons(pygame.display.Info(), screen, e.skeleton_frame.SkeletonData)
				pygame.display.update()
				pass
				
if __name__ == "__main__":
	main()
	