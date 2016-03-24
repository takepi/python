import cv2, numpy as np
from pykinect import nui

Depth = np.zeros((240, 320, 1), np.uint16)
Video = np.zeros((480, 640, 4), np.uint8)

def depth_frame_ready(frame):
	frame.image.copy_bits(Depth.ctypes.data)
	depth = cv2.flip(Depth, 1)
#	cv2.imshow("depth", depth)
#	print type(depth)

def video_frame_ready(frame):
	frame.image.copy_bits(Video.ctypes.data)
	video = cv2.flip(Video, 1)
	x = 40
	y = 40
	width = 640 - x * 2
	height = 480 - y * 2
	video = video[y:y + height, x:x + width]
	video = cv2.resize(video, (320, 240))
#	cv2.imshow("camera", video)

def nitika():
	depth = cv2.flip(np.array((2**16 - 1) * Depth / (2**8 - 1), np.uint8), 1)

	matrix = [
	[np.cos(0), -np.sin(0), 0], 
	[np.sin(0), np.cos(0), 12]
	]
	affine_matrix = np.float32(matrix)

	high = depth.shape[0]
	wide = depth.shape[1]
	size = (wide, high)
	
	depth = cv2.warpAffine(depth, affine_matrix, size, flags = cv2.INTER_LINEAR)
	
	ret, black = cv2.threshold(depth, 200, 255, cv2.THRESH_BINARY)
	ret, white = cv2.threshold(depth, 220, 255, cv2.THRESH_BINARY_INV)
	
	depth_near = ~(black ^ white)
	
	return depth_near
	
def mask():
	video = cv2.flip(Video, 1)
	videosize = video.shape
	n = nitika()
	mask = cv2.resize(n, (videosize[1], videosize[0]))
	maskman = cv2.bitwise_and(video, video, mask = mask)
	
#	hana = cv2.imread("hana", 1)
#	maskw = cv2.bitwise_not(mask)
#	maskedhana = cv2.bitwise_and(hana, hana, mask = maskw)
#	maskedman = cv2.bitwise_and(maskman, maskman, mask = maskw)
#	hanaman = cv2.bitwise_or(maskedman, maskhana)
	
#	print maskedman.shape
	
	cv2.imshow("masked", maskman)

def main():
	kinect = nui.Runtime()
	kinect.depth_frame_ready += depth_frame_ready
	kinect.video_frame_ready += video_frame_ready
	
	kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, 
							nui.ImageResolution.Resolution320x240, 
							nui.ImageType.Depth)
	kinect.video_stream.open(nui.ImageStreamType.video, 2, 
							nui.ImageResolution.Resolution640x480, 
							nui.ImageType.Color)
	
	cv2.namedWindow("masked", cv2.WINDOW_AUTOSIZE)
#	cv2.namedWindow("depth")
#	cv2.namedWindow("camera")
	
	while True:
		mask()
		if cv2.waitKey(10) == 27:
			break

	cv2.destroyAllWindows()
	kinect.close()

if __name__=="__main__":
	main()