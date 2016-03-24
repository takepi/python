import cv2
import numpy as np
import time
import traceback
import sys

def getColor(img, color):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	h_h = color + 10
	l_h = color - 10
	
	if l_h < 0:
		l_h = 180 + l_h
		h_color = np.array([h_h, 255, 255])
		l_color = np.array([l_h, 50, 50])
		red_color = [np.array([0, 50, 50]), np.array([180, 255, 255])]
		
		img_mask1 = cv2.inRange(hsv, red_color[0], h_color)
		img_mask2 = cv2.inRange(hsv, l_color, red_color[1])
		
		img_mask = img_mask1 + img_mask2
		
	else:
		h_color = np.array([h_h, 255, 255])
		l_color = np.array([l_h, 50, 50])
		
		img_mask = cv2.inRange(hsv, l_color, h_color)

	img_color = cv2.bitwise_and(img, img, mask = img_mask)
	
	return img_color
	
def removeNoise(img):
	kernel = np.ones((5, 5), np.uint8)
	
	dst = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
	
	return dst

def labeling(img):

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
	
	ret, labels, stats, centroids = cv2.connectedComponentsWithStats(th)
	
	areas = []
	for i in range(ret):
		if int(stats[i][4]) > 300:
			areas.append(i)
			
	rgbs = []
	for i in range(ret+1):
		j = 255/ret*i
		rgbs.append([255, 0, j])

	labeling = hsv
	for y in xrange(0, labeling.shape[0]):
		for x in xrange(0, labeling.shape[1]):
			if labels[y, x] == 0:
				pass
			elif labels[y, x] in areas:
				labeling[y, x] = rgbs[labels[y, x]]
			else:
				labeling[y, x] = [0, 0, 0]

	sortareas = []
	for i in areas:
		sortareas.append([int(stats[i][4]), i])
	sortareas = sorted(sortareas, reverse = True)

	areanums = [sortareas[i][1] for i in range(1, len(sortareas))]

	centers = []
	for i in areanums:
		x = int(centroids[i][0])
		y = int(centroids[i][1])
		centers.append([x, y])
				
	return labeling, centers
	
def circles(img, coodinate):
	for i in coodinate:
		cv2.circle(img, (i[0], i[1]), 10, (0, 0, 255), -1)
	
	return img
	
def main():
	color = 0
	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		img_mask = getColor(frame, color)
		img_clear = removeNoise(img_mask)
		img_label, centers = labeling(img_mask)
		img_circle = circles(img_label, centers)
		
		print type(frame)
		
		cv2.imshow("camera", frame)
#		cv2.imshow("clear", img_circle)
#		cv2.imshow("noisey", img_mask)
		
		k = cv2.waitKey(1)
		if k == ord("r"):
			color = 0
			print color
		elif k == ord("b"):
			color = 120
			print color
		elif k == 27:
			break
			
	cv2.destroyAllWindows()
	cap.release()
	
try:
	main()
except:
	print "---------------error------------------"
	print traceback.format_exc(sys.exc_info()[2])
	print "--------------------------------------"
	