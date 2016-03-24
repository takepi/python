import cv2
import numpy as np
import time
import traceback
import sys

def getColor(img, color):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	h_h = color + 7
	l_h = color - 7
	
	if l_h < 0:
		l_h = 180 + l_h
		h_h = h_h
		h_color = np.array([h_h, 255, 255])
		l_color = np.array([l_h, 100, 50])
		red_color = [np.array([0, 100, 50]), np.array([180, 255, 255])]
		
		img_mask1 = cv2.inRange(hsv, red_color[0], h_color)
		img_mask2 = cv2.inRange(hsv, l_color, red_color[1])
		
		img_mask = img_mask1 + img_mask2
		
	else:
		h_color = np.array([h_h, 255, 255])
		l_color = np.array([l_h, 150, 10])
		
		img_mask = cv2.inRange(hsv, l_color, h_color)

	img_color = cv2.bitwise_and(img, img, mask = img_mask)
	
	return img_color

def closeWorld(img):
	"""
	center = np.ones((img.shape[0], img.shape[1]/3), np.uint8)
	right = np.zeros((img.shape[0], img.shape[1]/3), np.uint8)
	left = np.zeros((img.shape[0], img.shape[1]-img.shape[1]/3*2), np.uint8)

	img_mask = np.hstack((left, center, right))

	img_close = cv2.bitwise_and(img, img, mask = img_mask)
	"""

	img_close = img[0 : img.shape[0], img.shape[1]/3 : img.shape[1]/3*2]

	return img_close

def removeNoise(img):
	kernel = np.ones((3, 3), np.uint8)
	
	dst = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
	
	return dst

def labeling(img, minsize, maxsize):

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
	
	ret, labels, stats, centroids = cv2.connectedComponentsWithStats(th)
	
	areas = []
	for i in range(ret):
		if int(stats[i][4]) >= minsize:
			if int(stats[i][4]) <= maxsize:
				areas.append(i)

	sortareas = []
	for i in areas:
		sortareas.append([int(stats[i][4]), i])
	sortareas = sorted(sortareas, reverse = True)

	areanums = [sortareas[i][1] for i in range(len(sortareas))]

	centers = []
	for i in areanums:
		x = int(centroids[i][0])
		y = int(centroids[i][1])
		centers.append([x, y])
				
	return centers
	
def circles(img, coodinate):
	for i in coodinate:
		cv2.circle(img, (i[0], i[1]), 10, (0, 0, 255), -1)
	
	return img

def getPole(img, pole):

	sizes = {"c" : [300, 1000], "b" : [100, 300], "a" : [10, 100]} 

	if pole == "c":
		img_close = img
	else:
		img_close = closeWorld(img)

	img_red = getColor(img_close, 0)
	img_blue = getColor(img_close, 110)

	gray_red = cv2.cvtColor(img_red, cv2.COLOR_BGR2GRAY)
	gray_blue = cv2.cvtColor(img_blue, cv2.COLOR_BGR2GRAY)

	ret, th_red = cv2.threshold(gray_red, 0, 255, cv2.THRESH_BINARY)
	ret, th_blue = cv2.threshold(gray_blue, 0, 255, cv2.THRESH_BINARY)

	img_mask = th_red + th_blue

	img_clear = removeNoise(img_mask)
	img_color = cv2.bitwise_and(img_close, img_close, mask = img_clear)

	center = labeling(img_color, sizes[pole][0], sizes[pole][1])

	if len(center) < 2:
		point = []
	else:	
		point = [[(center[0][0]+center[1][0])/2, (center[0][1]+center[1][1])/2]]

	ypoints = []
	if len(center) != 0:
		for i in range(len(center)):
			ypoints.append([center[i][1], i])

		hpoint = min(ypoints)
		y = center[hpoint[1]][1]
		x = center[hpoint[1]][0]
		b, g, r = img_color[y, x]
		hcolor = max(b, g, r)

		if hcolor == b:
			pcolor = "blue"
		elif hcolor == r:
			pcolor = "red"
		
	else:
		pcolor = None

	return img_color, point, pcolor

def main():
	pole = "c"
	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		
		img_c1, centers, pcolor = getPole(frame, pole)
#		img_circle = circles(img_c1, centers)
		print pcolor

		cv2.imshow("pole", img_c1)

		k = cv2.waitKey(1)
		if k == ord("a"):
			pole = "a"
			print pole
		elif k == ord("b"):
			pole = "b"
			print pole
		elif k == ord("c"):
			pole = "c"
			print pole
		elif k == ord("s"):
			img_red = getColor(frame, 0)
			img_blue = getColor(frame, 110)

			gray_red = cv2.cvtColor(img_red, cv2.COLOR_BGR2GRAY)
			gray_blue = cv2.cvtColor(img_blue, cv2.COLOR_BGR2GRAY)

			ret, th_red = cv2.threshold(gray_red, 0, 255, cv2.THRESH_BINARY)
			ret, th_blue = cv2.threshold(gray_blue, 0, 255, cv2.THRESH_BINARY)

			img_mask = th_red + th_blue
			img_clear = removeNoise(img_mask)
			
			cv2.imwrite("pole.jpg", img_clear)
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
	
