import cv2
import numpy as np
import functools as ft
import time
import traceback
import sys
import gc

def pole(frame, color):
	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	h_h = color + 7
	l_h = color - 7

	if l_h < 0:
		l_h = 180 + l_h
		h_color = np.array([l_h, 50, 50])
		l_color = np.array([h_h, 255, 255])
		red_color = [np.array([0, 50, 50]), np.array([180, 255, 255])]
		img_mask1 = cv2.inRange(hsv, red_color[0], l_color)
		img_mask2 = cv2.inRange(hsv, h_color, red_color[1])

		img_mask = img_mask1 + img_mask2

	else:
		h_color = np.array([h_h, 255, 255])
		l_color = np.array([l_h, 50, 50])
		img_mask = cv2.inRange(hsv, l_color, h_color)
		
	kernel = np.ones((5,5),np.uint8)

	dst = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
	dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)

	img_color = cv2.bitwise_and(frame, frame, mask = dst)
	
	moments = cv2.moments(dst)
	if moments["m00"] != 0:
		xcenter = int(moments["m10"]/moments["m00"])
		ycenter = int(moments["m01"]/moments["m00"])
		cv2.circle(img_color, (xcenter, ycenter), 5, (255, 255, 255), -1)
		
	return img_color

def mouse(event, x, y, flag, frame):

	global color

	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	if event == cv2.EVENT_LBUTTONDOWN:
		color = frame[y, x][0]
		print "color" ,frame[y, x]

color = 0

def main():
	cap = cv2.VideoCapture(1)
	while True:
		ret, frame = cap.read()
		img = pole(frame, color)
		
		cv2.setMouseCallback("color", mouse, frame)

		cv2.imshow("color", frame)
		cv2.imshow("camera", img)

#		gc.set_debug(gc.DEBUG_LEAK)
		
		if cv2.waitKey(1) == 27:
			break

	cv2.destroyAllWindows()
	cap.release()

try:
	main()
except:
	print "---------------error------------------"
	print traceback.format_exc(sys.exc_info()[2])
	print "--------------------------------------"
