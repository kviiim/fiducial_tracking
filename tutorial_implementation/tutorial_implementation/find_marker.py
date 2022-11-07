import enum
from turtle import window_height
import cv2
import numpy as np
import operator

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

K_D = 100
K_M = 1200

class Node():
    def __init__(self, x, y, D, M):
        """
        color is the color of the pixel in bgr
        D is the range of directions of the gradient
        M in the range of magnitudes of the gradient
        """
        self.D = D
        self.M = M
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        print('Node- D: ', self.D, ' M: ', self.M)

class Edge():
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __repr__(self) -> str:
        print('Edge- ', self.weight)

class Segment():
    def __init__(self, endpoint1, endpoint2, M, D):
        self.endpoint1 = endpoint1
        self.endpoin2 = endpoint2
        self.center = ((endpoint1[0]+endpoint2[0])/2, (endpoint1[1]+endpoint2[1])/2)
        self.M = M
        self.D = D


class FindMarker():
    def __init__(self):
        segments_not_class = np.array([[0, 0, 0, 0]], dtype=np.float32)

    def detector(self, image):
        '''
        Identify tag shaped items in a given image
        '''
        #create image graph
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image_nodes = np.zeros(image.shape[0] * image.shape[1], dtype=Node)
        edges = np.array([], dtype=Edge)
        segments = []
        # create a set of components
        components = set()
        #process each pixel
        for [y,row] in enumerate(image):
            for [x,pixel] in enumerate(row):
                #calculate gradient of pixel
                if x != len(row) -1 | x != 0:
                    x_grad = float(image[y][x+1]) - float(image[y][x-1])
                else: 
                    # TODO: Fix this
                    x_grad = 0.1
                if y != len(image) -1 | y != 0:
                    y_grad = float(image[y+1][x]) - float(image[y-1][x])
                else:
                    # TODO: Fix this
                    y_grad = 0.1
                #calculate direction and magnitude of gradient
                D = np.arctan2(y_grad, x_grad)
                M = np.sqrt(x_grad**2 + y_grad**2)

                idx = y * len(row) + x
                #create pixel node in graph
                node = Node(y,x, D, M)
                image_nodes[idx] = node

                current_node = image_nodes[idx]
                if x != 0: 
                    # if x is not zero we can find the left pixel
                    left_node = image_nodes[idx - 1]
                    edges = np.append(edges, Edge(left_node, current_node, abs(current_node.D - left_node.D)))

                if y != 0:
                    # if y is not zero we can find the top pixel
                    top_node = image_nodes[idx - len(row)]
                    edges = np.append(edges, Edge(top_node, current_node, abs(current_node.D - top_node.D)))

                # if neither is zero we can find the diagonal left pixel 
                if x != 0 & y != 0:
                    top_left = image_nodes[idx - len(row) - 1]
                    top_left.edges[current_node] = abs(current_node.D - top_left.D)
                    edges = np.append(edges, Edge(top_left, current_node, abs(current_node.D - top_left.D)))

        edges = sorted(edges, key=lambda edge : edge.weight)
        #find segments
        for edge in edges:
            segment1 = None
            segment2 = None
            segment1_in_semgents = False
            segment2_in_segments = False
            for [idx,segment] in enumerate(segments):
                if edge.node1 in segment:
                    segment1 = segment
                    segment1_in_semgents = True
                if edge.node2 in segment:
                    segment2 = segment
                    segment2_in_segments = True
                # if segment1 and segment2:
                #     break
            
            if not segment1:
                segment1 = {edge.node1}
            if not segment2:
                segment2 = {edge.node2}
            if segment1 != segment2:
                union_segment = segment1.union(segment2)

                #send help
                union_M_max = max(union_segment, key=operator.attrgetter('M')).M
                union_M_min = min(union_segment, key=operator.attrgetter('M')).M
                union_D_max = max(union_segment, key=operator.attrgetter('D')).D
                union_D_min = min(union_segment, key=operator.attrgetter('D')).D

                segment1_M_max = max(segment1, key=operator.attrgetter('M')).M
                segment1_M_min = min(segment1, key=operator.attrgetter('M')).M
                segment1_D_max = max(segment1, key=operator.attrgetter('D')).D
                segment1_D_min = min(segment1, key=operator.attrgetter('D')).D

                segment2_M_max = max(segment2, key=operator.attrgetter('M')).M
                segment2_M_min = min(segment2, key=operator.attrgetter('M')).M
                segment2_D_max = max(segment2, key=operator.attrgetter('D')).D
                segment2_D_min = min(segment2, key=operator.attrgetter('D')).D

                if (union_D_max - union_D_min) <= min((segment1_D_max - segment1_D_min), (segment2_D_max-segment2_D_min)) + (K_D/len(union_segment)) and \
                    (union_M_max - union_M_min) <= min((segment1_M_max - segment1_M_min), (segment2_M_max-segment2_M_min)) + (K_M/len(union_segment)):
                    #union!
                    if segment1_in_semgents:
                        segments.remove(segment1)
                    if segment2_in_segments:
                        segments.remove(segment2)
                    segments.append(union_segment)
                else:
                    if not segment1_in_semgents:
                        segments.append(segment1)
                    if not segment2_in_segments:
                        segments.append(segment2)
        
        # plotting
        colors = ['or', 'ob', 'og', 'oy', 'oc', 'ok']
        colors_append = ['ok' for i in range (len(segments))]
        colors = colors + colors_append
        for [idx,segment] in enumerate(segments):
            xs = []
            ys = []
            for node in segment:
                xs.append(node.x)
                ys.append(node.y)
                # print(node.x, node.y)
            plt.plot(ys,xs,'o')
        plt.gca().invert_yaxis()
        plt.show()
        print(len(segments))

        segments_class = []
        for segment in segments:
            segments_class.append








    def identifier(self, potential_tag):
        '''
        For a potential tag, identify it's fiducial ID or reject it
        '''
        pass
