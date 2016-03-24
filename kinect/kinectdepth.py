from pykinect import nui
import cv2
import numpy as np

def depth_frame_ready(frame):
    depth = np.empty((240, 320, 1), np.uint16)
    frame.image.copy_bits(depth.ctypes.data)
    depth = cv2.flip(depth, 1)
    cv2.imshow("depth", depth)

def main():
    
	kinect = nui.Runtime()

	kinect.depth_frame_ready += depth_frame_ready

	kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, 
							nui.ImageResolution.Resolution320x240, 
							nui.ImageType.Depth)

    cv2.namedWindow("depth", cv2.WINDOW_AUTOSIZE)
#	cv2.namedWindow("depth", cv2.WINDOW_KEEPRATIO|cv2.WINDOW_NORMAL)

	cv2.waitKey(0)

	cv2.destroyAllWindows()
	kinect.close()

if __name__=="__main__":
    main()