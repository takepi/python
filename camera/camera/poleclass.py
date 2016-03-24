import cv2
import numpy as np
import ConfigParser

class Pole:

	def __init__(self, ini):

		inifile = ConfigParser.SafeConfigParser()
		inifile.read(ini)
		self.rscope = int(inifile.get("Red", "scope"))
		self.rmax_s = int(inifile.get("Red", "max_s"))
		self.rmax_v = int(inifile.get("Red", "max_v"))
		self.rmin_s = int(inifile.get("Red", "min_s"))
		self.rmin_v = int(inifile.get("Red", "min_v"))
		self.bscope = int(inifile.get("Blue", "scope"))
		self.bmax_s = int(inifile.get("Blue", "max_s"))
		self.bmax_v = int(inifile.get("Blue", "max_v"))
		self.bmin_s = int(inifile.get("Blue", "min_s"))
		self.bmin_v = int(inifile.get("Blue", "min_v"))

	def getColor(self, img, color):

		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		if color < self.bscope:
			h_h = color + self.rscope
			l_h = color + 180 - self.rscope
			h_color = np.array([h_h, self.rmax_s, self.rmax_v])
			l_color = np.array([l_h, self.rmin_s, self.rmin_v])
			red_color = [np.array([0, self.rmin_s, self.rmin_v]), np.array([180 ,self.rmax_s, self.rmax_v])]

			img_mask1 = cv2.inRange(hsv, red_color[0], h_color)
			img_mask2 = cv2.inRange(hsv, l_color, red_color[1])

			img_mask = img_mask1 + img_mask2

		else:
			h_h = color + self.bscope
			l_h = color - self.bscope
			h_color = np.array([h_h, self.bmax_s, self.bmax_v])
			l_color = np.array([l_h, self.bmin_s, self.bmin_v])

			img_mask = cv2.inRange(hsv, l_color, h_color)

		img_color = cv2.bitwise_and(img, img, mask = img_mask)

		return img_color

	def closeWorld(self, img):
		
		img_close = img[0 : img.shape[0], img.shape[1]/3 : img.shape[1]/3*2]

		return img_close
	
	def removeNoise(self, img):

		kernel = np.ones((3, 3), np.uint8)

		dst = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
		dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)

		return dst

	def labeling(self, img, minsize, maxsize):
	
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

		if ret > 1:
			area = max([int(stats[i][4]) for i in range(1, ret)])
		else:
			area = None

		return centers, area

	def circles(self, img, coodinate):

		for i in coodinate:
			cv2.circle(img, (i[0], i[1]), 10, (0, 0, 255), -1)

	def getPole(self, pole, img):

		sizes = {"c" : [250, 1000], "b" : [80, 250], "a" : [10, 80]}

		if pole == "c":
			img_close = img
		else:
			img_close = self.closeWorld(img)

		img_red = self.getColor(img_close, 0)
		img_blue = self.getColor(img_close, 110)

		gray_red = cv2.cvtColor(img_red, cv2.COLOR_BGR2GRAY)
		gray_blue = cv2.cvtColor(img_blue, cv2.COLOR_BGR2GRAY)

		ret, th_red = cv2.threshold(gray_red, 0, 255, cv2.THRESH_BINARY)
		ret, th_blue = cv2.threshold(gray_blue, 0, 255, cv2.THRESH_BINARY)

		img_mask = th_red + th_blue

		img_clear = self.removeNoise(img_mask)
		img_color = cv2.bitwise_and(img_close, img_close, mask = img_clear)

		center, area = self.labeling(img_color, sizes[pole][0], sizes[pole][1])

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

			cpoint = [[x, y]]

			if hcolor == b:
				pcolor = "blue"
			elif hcolor == r:
				pcolor = "red"

		else:
			pcolor = None
			cpoint = []

		return img_color, cpoint, pcolor, area

