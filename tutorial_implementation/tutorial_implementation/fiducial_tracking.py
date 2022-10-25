import cv2
from cv_bridge import CvBridge

import apriltag

from rclpy.node import Node
import rclpy

from sensor_msgs.msg import Image
import numpy as np


class ProcessTag(Node):
    '''
    Node which handles neato motion
    '''
    def __init__(self):
        super().__init__('send_message_node')
        # Create a timer that fires ten times per second
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.run_loop)
        # Publisher which sends neato velocity commands
        self.publisher = self.create_publisher(Image, 'fiducial_image', 10)
        self.subscriber = self.create_subscription(Image, "camera/image_raw", self.process_image, 10)
        # Stores key which has been pressed last
        self.detected_image = []
        self.bridge = CvBridge()                    # used to convert ROS messages to OpenCV


    def process_image(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # print("[INFO] detecting AprilTags...")
        options = apriltag.DetectorOptions(families="tag36h11")
        detector = apriltag.Detector(options)
        results = detector.detect(gray)
        print("[INFO] {} total AprilTags detected".format(len(results)))

        for r in results:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
            # draw the bounding box of the AprilTag detection
            cv2.line(image, ptA, ptB, (0, 255, 0), 2)
            cv2.line(image, ptB, ptC, (0, 255, 0), 2)
            cv2.line(image, ptC, ptD, (0, 255, 0), 2)
            cv2.line(image, ptD, ptA, (0, 255, 0), 2)
            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # print("[INFO] tag family: {}".format(tagFamily))
        self.detected_image = image


    def run_loop(self):
        if len(self.detected_image) != 0:
            image_message = self.bridge.cv2_to_imgmsg(self.detected_image, encoding="passthrough")
            self.publisher.publish(image_message)





def main(args=None):
    rclpy.init(args=args)      # Initialize communication with ROS
    node = ProcessTag()   # Create our Node
    rclpy.spin(node)           # Run the Node until ready to shutdown
    rclpy.shutdown()           # cleanup


if __name__ == '__main__':
    main()
