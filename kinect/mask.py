import cv2
import numpy as np

red = cv2.imread("red.png", 1)
maru = cv2.imread("maru.png", 0)
komaru = cv2.imread("komaru.png", 0)

imgsize = red.shape
komaru = cv2.resize(komaru, (imgsize[1], imgsize[0]))

a = np.zeros((imgsize[0]/2, imgsize[1]), np.uint8)
b = np.ones((imgsize[0]/2, imgsize[1]), np.uint8)
c = np.vstack((a, b))

mask = cv2.bitwise_and(red, red, mask = c)

cv2.imshow("a", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()