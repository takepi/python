import cv2
import numpy as np

cap = cv2.VideoCapture(0)

x = 300
y = 200
w = 100
h = 100
track_window = (x, y, w, h)

ret, frame = cap.read()

roi = frame[y:y+h, x:x+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
img_mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255, 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], img_mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while True:
	ret, farme = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

	x, y, w, h = track_window
	img_dst = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)
	cv2.imshow("aaa", img_dst)

	print "a"

	if cv2.waitKey(1) == 27:
		break

cv2.destroyAllWindows()
cap.release()
