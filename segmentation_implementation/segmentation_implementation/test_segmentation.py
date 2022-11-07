import image_segmentation
import cv2

#import an image and run segmentation on it
image_segmentation = image_segmentation.Segment_Image()
image = cv2.imread('segmentation_implementation/segmentation_implementation/tags/sideways_t.png')
image_segmentation.detector(image)