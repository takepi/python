from pykinect import nui
import cv2
import numpy as np

def video_frame_ready(frame):
    video = np.empty((480, 640, 4), np.uint8)
    frame.image.copy_bits(video.ctypes.data)
    video = cv2.flip(video, 1)
    cv2.imshow("camera", video)

def main():

    kinect = nui.Runtime()

    kinect.video_frame_ready += video_frame_ready
    
    kinect.video_stream.open(nui.ImageStreamType.Video, 2, 
                             nui.ImageResolution.resolution_640x480, 
                             nui.ImageType.Color)
    
    cv2.namedWindow("camera", cv2.WINDOW_AUTOSIZE)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
    kinect.close()

if __name__=="__main__":
    main()