import find_marker
import cv2

find_marker = find_marker.FindMarker()
image = cv2.imread('/home/annabelle/ros2_ws/src/fiducial_tracking/tutorial_implementation/tutorial_implementation/tags/tag36_11_00372.png')
print(image.shape)
find_marker.detector(image)