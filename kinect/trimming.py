import cv2

robo = cv2.imread("hana.jpg", 1)
size = robo.shape

x = 5
y = 5
width = size[1] - 10
height = size[0] - 10

newrobo = robo[y:y + height, x:x + width]
cv2.imshow("robo", robo)
cv2.imshow("new", newrobo)

cv2.waitKey(0)
cv2.destroyAllWindows()