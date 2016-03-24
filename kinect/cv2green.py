import cv2
import numpy as np

white_img = np.tile(np.uint8([255, 0, 0]),(200, 200, 1))
black_img = np.tile(np.uint8([0, 0, 255]), (200, 200, 1))

masked_img = white_img + black_img	

cv2.namedWindow("masked", cv2.WINDOW_AUTOSIZE)
cv2.imshow("masked", masked_img)

cv2.waitKey(0)

cv2.destroyAllWindows()