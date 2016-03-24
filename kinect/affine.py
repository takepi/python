import cv2, numpy as np, time

komaru = cv2.imread("komaru.png", 1)

rad = 0

high = komaru.shape[0]
wide = komaru.shape[1]
size = (wide, high)

cv2.imshow("komaru", komaru)

i = -5
matrix = [
[np.cos(rad), -np.sin(rad), i], 
[np.sin(rad), np.cos(rad), i]
]
affine_matrix = np.float32(matrix)

komaru_zure = cv2.warpAffine(komaru, affine_matrix, size, flags = cv2.INTER_LINEAR)
cv2.imshow("komaru_zure", komaru_zure)
time.sleep(0.1)

cv2.waitKey(0)
cv2.destroyAllWindows()
