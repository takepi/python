import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)
while True:
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	h = np.array([130, 255, 255])
	l = np.array([110, 50, 50])

	img = cv2.inRange(hsv, l, h)

	kernel = np.ones((5,5),np.uint8)

	dst = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
	
	blue = cv2.bitwise_and(frame, frame, mask = dst)

	"""
	
	n, label = cv2.connectedComponents(dst)

	rgbs = np.random.randint(0, 255, [n+1, 3])
	labeling = frame
	
	for y in xrange(0, img.shape[0]):
		for x in xrange(0, img.shape[1]):
			if label[y, x] > 0:
				labeling[y, x] = rgbs[label[y, x]]
			else:
				labeling[y, x] = [0, 0, 0]
	"""	

	cv2.imshow("camera", frame)
	cv2.imshow("blue", blue)

	if cv2.waitKey(1) == 27:
		break
	
cv2.destroyAllWindows()
cap.release()
