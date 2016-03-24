import cv2

face_cascade = cv2.CascadeClassifier("C:\Users\takeshi\Downloads\opencv\build\share\OpenCV\haarcascades\haarcascade_frontalface_default.xml")

print face_cascade

face = cv2.imread("kato.jpg")
img = cv2.imread("iwakura.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 1, minSize = (100, 100))

print face