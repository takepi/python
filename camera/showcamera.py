import cv2

cap = cv2.VideoCapture(1)

while True:
	ret, frame = cap.read()

#	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	cv2.imshow("camera", frame)
#	cv2.imshow("gray", gray)

	k = cv2.waitKey(1)
	if k == 27:
		break
	elif k == ord("s"):
		cv2.imwrite("pole.jpg", frame)

cap.release()
cv2.destroyAllWindows()
