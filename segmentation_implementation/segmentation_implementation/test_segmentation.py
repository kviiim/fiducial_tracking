import image_segmentation
import cv2

#import an image and run segmentation on it
image_segmentation = image_segmentation.Segment_Image()
image = cv2.imread('/home/kat/ros2_ws/src/fiducial_tracking/tutorial_implementation/tutorial_implementation/tags/sideways_t.png')
image_segmentation.detector(image)