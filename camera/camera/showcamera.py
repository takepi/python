import cv2

cap = cv2.VideoCapture(0)

while True:
#	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	ret, frame = cap.read()
	cv2.imshow("camera", frame)
#	cv2.imshow("gray", gray)

	k = cv2.waitKey(1)
	if k == 27:
		break

#cap.release()
cv2.destroyAllWindows()
