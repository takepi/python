import cv2, numpy as np
from pykinect import nui
import traceback, sys

def nitika(im):

    im = np.array((2**16 - 1) * im / (2**8 - 1), np.uint8)

    ret, black = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
    ret, white = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY_INV)

    return white

def mask(mask, img):
    img_masked = cv2.bitwise_and(img, img, mask = mask)
#    cv2.imshow("masked", img_masked)

def depth_frame_ready(frame):
    depth = np.empty((240, 320, 1), np.uint16)
    frame.image.copy_bits(depth.ctypes.data)
    depth = cv2.flip(depth, 1)
    cv2.imshow("depth", depth)

    nitika(depth)

def video_frame_ready(frame):
    video = np.empty((480, 640, 4), np.uint8)
    frame.image.copy_bits(video.ctypes.data)
    video = cv2.flip(video, 1)
    cv2.imshow("camera", video)

#    mask(video, nitika


def main():

	try:
		kinect = nui.Runtime()
	except:
		print traceback.format_exc(sys.exc_info()[2])
	kinect.depth_frame_ready += depth_frame_ready
	kinect.video_frame_ready += video_frame_ready

	kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, 
                             nui.ImageResolution.Resolution320x240, 
                             nui.ImageType.Depth)
	kinect.video_stream.open(nui.ImageStreamType.video, 2, 
                             nui.ImageResolution.Resolution640x480, 
                             nui.ImageType.Color)

#    cv2.namedWindow("masked", cv2.WINDOW_AUTOSIZE)
#    cv2.namedWindow("black", cv2.WINDOW_AUTOSIZE)
#    cv2.namedWindow("white", cv2.WINDOW_AUTOSIZE)
	cv2.namedWindow("camera", cv2.WINDOW_AUTOSIZE)
	cv2.namedWindow("depth", cv2.WINDOW_AUTOSIZE)

	while True:

		if cv2.waitKey(10) == 27:
			break

	cv2.destroyAllWindows()
	kinect.close()

if __name__=="__main__":
	main()