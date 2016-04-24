import cv2, numpy as np

d = cv2.imread("depth.png", -1)
hana = cv2.imread("hana.jpg")

width, height = d.shape[:2]

dd = d[:, :, :3]
#dd = cv2.cvtColor(dd, cv2.CV_GRAY2BGR)
dd = d / 255.0

d = d[:, :, :3]

hana[0:height, 0:width] *= 1 - d
hana[0:height, 0:width] += d * dd

cv2.imshow("d", hana)

cv2.waitKey(0)
cv2.destroyAllWindows()