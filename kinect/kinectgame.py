from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters
from pygame.color import THECOLORS

import pygame
from pygame.locals import *
import time
import itertools
import math
import threading

KINECTEVENT = pygame.USEREVENT
WINDOW_SIZE = 640, 480

SKELETON_COLORS = [THECOLORS["green"], 
				   THECOLORS["red"], 
				   THECOLORS["blue"], 
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
		
def draw_skeleton_data(dispInfo, screen, pSkelton, index, positions, width = 10):
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
			pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
			
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_ARM)
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_ARM)
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_LEG)
			draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_LEG)
		
def getPoint(dispInfo, screen, skeletons):
	screen.fill((255, 150, 0))
	player1 = ["x", "y"]
	player2 = ["x", "y"]
	count = 0
	for index, data in enumerate(skeletons):
		if data.eTrackingState == SkeletonTrackingState.TRACKED:
			count += 1
			
			HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h)
			
			draw_skeleton_data(dispInfo, screen, data, count, SPINE, 10)
			pygame.draw.circle(screen, SKELETON_COLORS[count], (int(HeadPos[0]), int(HeadPos[1])), 15, 0)
			
			draw_skeleton_data(dispInfo, screen, data, count, LEFT_ARM)
			draw_skeleton_data(dispInfo, screen, data, count, RIGHT_ARM)
			draw_skeleton_data(dispInfo, screen, data, count, LEFT_LEG)
			draw_skeleton_data(dispInfo, screen, data, count, RIGHT_LEG)
			
			center = skeleton_to_depth_image(data.SkeletonPositions[JointId.ShoulderCenter], dispInfo.current_w, dispInfo.current_h)
			rightHand = skeleton_to_depth_image(data.SkeletonPositions[JointId.HandRight], dispInfo.current_w, dispInfo.current_h)
			rHandx = rightHand[0] - center[0]
			rHandy = rightHand[1] - center[1]
			rHandegree = int(math.degrees(math.atan2(rHandy,rHandx)))
			ratio = int(math.fabs(math.sqrt(rHandy**2+rHandx**2)))
			if count == 1:
				player1[0] = rHandx
				player1[1] = rHandy
			elif count == 2:
				player2[0] = rHandx
				player2[1] = rHandy
#			print "player1", player1
#			print "player2", player2
#			print "count", count
			
	return count, player1, player2
		
def moveChara(dispInfo, screen, skeletons, dango_rect, otya_rect):
	count, player1, player2 = getPoint(dispInfo, screen, skeletons)
	
	if dango_rect.center[0] <= 0:
		player1 = [100, 0]
	elif dango_rect.center[0] >= 640:
		player1 = [-100, 0]
	if dango_rect.center[1] <= 0:
		player1 = [0, 100]
	elif dango_rect.center[1] >= 480:
		player1 = [0, -100]

	if otya_rect.center[0] <= 0:
		player2 = [100, 0]
	elif otya_rect.center[0] >= 640:
		player2 = [-100, 0]
	if otya_rect.center[1] <= 0:
		player2 = [0, 100]
	elif otya_rect.center[1] >= 480:
		player2 = [0, -100]
		
	if count == 1:
		dango_rect.move_ip(player1[0] / 50, player1[1] / 50)
	elif count == 2:
		dango_rect.move_ip(player1[0] / 50, player1[1] / 50)
		otya_rect.move_ip(player2[0] / 50, player2[1] / 50)
	
#	print dango_rect.center
	
def main():
	pygame.init()

	screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
	pygame.display.set_caption("Skeleton")
	screen.fill(pygame.color.THECOLORS["black"])
	
	dango = pygame.image.load("dango.png").convert()
	colorkey = dango.get_at((0, 0))
	dango.set_colorkey(colorkey, RLEACCEL)
	dango_rect = dango.get_rect()
	dango_rect.center = (160, 240)

	otya = pygame.image.load("otya.png").convert()
	colorkey = otya.get_at((0, 0))
	otya.set_colorkey(colorkey, RLEACCEL)
	otya_rect = otya.get_rect()
	otya_rect.center = (480, 240)
	
	with nui.Runtime() as kinect:
		kinect.skeleton_engine.enabled = True
		kinect.skeleton_frame_ready += post_frame
	
		while True:
			screen.blit(dango, dango_rect)
			screen.blit(otya, otya_rect)
			pygame.display.update()
			
			e = pygame.event.wait()
			if e.type == pygame.QUIT:
				break
				
			elif e.type == KEYDOWN:
				if e.key == K_q:
					break
				
			elif e.type == KINECTEVENT:
#				draw_skeletons(pygame.display.Info(), screen, e.skeleton_frame.SkeletonData)
				moveChara(pygame.display.Info(), screen, e.skeleton_frame.SkeletonData, dango_rect, otya_rect)
				
if __name__ == "__main__":
	main()
	