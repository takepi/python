import cv2
import numpy as np
import time

def valprint(**val):
	for i in val:
		print type(val[i])
		if type(val[i]) == np.ndarray:
			cv2.imshow("i", val[i])
		print i, " : ", val[i]
	
valprint(A = 1, B = 2, a = np.array(3))

time.sleep(3)