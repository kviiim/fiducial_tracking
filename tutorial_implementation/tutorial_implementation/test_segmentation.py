# import find_marker_no_classes as find_marker
import find_marker
import cv2

find_marker = find_marker.FindMarker()
image = cv2.imread('/home/kat/ros2_ws/src/fiducial_tracking/tutorial_implementation/tutorial_implementation/tags/sideways_t.png')
print(image.shape)
find_marker.detector(image)