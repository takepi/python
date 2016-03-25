import cv2
import numpy as np
import time

src = cv2.imread("pole.jpg")

hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

ret, labels, stats, centroids = cv2.connectedComponentsWithStats(th)

areas = []
for i in range(ret):
	if int(stats[i][4]) > 0:
		if int(stats[i][4]) < 9999:
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
"""
for y in xrange(0, labeling.shape[0]):
	for x in xrange(0, labeling.shape[1]):
		if labels[y, x] > 0:
			labeling[y, x] = rgbs[labels[y, x]]
		else:
			labeling[y, x] = [0, 0, 0]
"""

font = cv2.FONT_HERSHEY_PLAIN

for i in areas:
	cv2.putText(labeling, str(stats[i][4]), (int(centroids[i][0]), int(centroids[i][1])), font, 1, [255, 255, 255])

cv2.imshow("labeling", labeling)

print "ret", ret
print "stats", stats
print "centroids", centroids
print "areas", areas

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

cv2.waitKey(0)
