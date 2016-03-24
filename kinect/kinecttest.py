import numpy, cv2, traceback, sys
from pykinect import nui

def video_frame_ready(frame):
	video = np.empty((480, 640, 4), np.uint8)
	frame.image.copy_bits(video.ctypes.data)
	video = cv2.flip(video, 1)
	cv2.imshow("camera", video)
	
def main():

	try:
		kinect = nui.Runtime()
	except:
		print "--------------------------------------"
		print traceback.format_exc(sys.exc_info()[2])
		print "--------------------------------------"
		
	kinect.depth_frame_ready += depth_frame_ready
	kinect.video_frame_ready += video_frame_ready
	
	kinect.video_stream.open(nui.ImageStreamType.video, 2, 
                             nui.ImageResolution.Resolution640x480, 
                             nui.ImageType.Color)
							 
	cv2.namedWindow("camera", cv2.WINDOW_AUTOSIZE)
	
	while True:

		if cv2.waitKey(10) == 27:
			break

	cv2.destroyAllWindows()
	kinect.close()

if __name__=="__main__":
	main()