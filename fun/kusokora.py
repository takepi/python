import cv2

cascadepath = "C:\Users\takeshi\Downloads\opencv\build\share\OpenCV\haarcascades\haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(cascadepath)

img = cv2.imread("iwakura.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 1, minSize = (10, 10))
faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 1, minSize = (10, 10))

if len(face) > 0:
	for rect in face:
		cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 0), thickness = 2)
		
cv2.imshow("kao", img)