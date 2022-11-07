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
        x is the pixel x coordinate
        y is the pixel y coordinate
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
    '''
    Stores edges between adjacent nodes with a weight
    '''
    def __init__(self, node1, node2, weight):
        '''
        node1 is a Node object
        node2 is an adjacent Node object
        weight is an integer weight of that edge 
        '''
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __repr__(self) -> str:
        print('Edge- ', self.weight)

class Segment_Image():
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
                #calculate x gradient of pixel
                if x != len(row) -1 | x != 0:
                    x_grad = float(image[y][x+1]) - float(image[y][x-1])
                elif x == 0: 
                    x_grad = float(image[y][x+1]) - float(image[y][x])
                else:
                    x_grad = float(image[y][x]) - float(image[y][x-1])

                #calculate y gradient of pixel
                if y != len(image) -1 | y != 0:
                    y_grad = float(image[y+1][x]) - float(image[y-1][x])
                elif y == 0:
                    y_grad = float(image[y+1][x]) - float(image[y][x])
                else:
                    y_grad = float(image[y][x]) - float(image[y-1][x])

                #calculate direction and magnitude of gradient
                D = np.arctan2(y_grad, x_grad)
                M = np.sqrt(x_grad**2 + y_grad**2)

                idx = y * len(row) + x
                #create pixel node in graph
                node = Node(y,x, D, M)
                image_nodes[idx] = node

                current_node = image_nodes[idx]
                #create edges based on adjacent nodes
                # if x is not zero we can find the left pixel
                if x != 0: 
                    left_node = image_nodes[idx - 1]
                    edges = np.append(edges, Edge(left_node, current_node, abs(current_node.D - left_node.D)))
                    
                # if y is not zero we can find the top pixel
                if y != 0:
                    top_node = image_nodes[idx - len(row)]
                    edges = np.append(edges, Edge(top_node, current_node, abs(current_node.D - top_node.D)))

                # if neither is zero we can find the diagonal left pixel 
                if x != 0 & y != 0:
                    top_left = image_nodes[idx - len(row) - 1]
                    top_left.edges[current_node] = abs(current_node.D - top_left.D)
                    edges = np.append(edges, Edge(top_left, current_node, abs(current_node.D - top_left.D)))
 
        #sort the edges by weight
        edges = sorted(edges, key=lambda edge : edge.weight)
        #find line segments based on nodes with similar gradients
        for edge in edges:
            segment1 = None
            segment2 = None
            segment1_in_semgents = False
            segment2_in_segments = False
            #check if current nodes are already in a line segment
            for [idx,segment] in enumerate(segments):
                if edge.node1 in segment:
                    segment1 = segment
                    segment1_in_semgents = True
                if edge.node2 in segment:
                    segment2 = segment
                    segment2_in_segments = True
            #if the nodes are not in a segment, create one
            if not segment1:
                segment1 = {edge.node1}
            if not segment2:
                segment2 = {edge.node2}

            #do nothing if the nodes are already part of a segment
            if segment1 != segment2:

                #calculate what the union of the two segments would be
                union_segment = segment1.union(segment2)

                #find the minimum and maximum of each segments gradient magnitude and direction
                #optimizing our code would aim to make this cleaner, as this requires a lot of time
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

                #if the gradient's magnitude and direction are within similar ranges, we have found a union
                if (union_D_max - union_D_min) <= min((segment1_D_max - segment1_D_min), (segment2_D_max-segment2_D_min)) + (K_D/len(union_segment)) and \
                    (union_M_max - union_M_min) <= min((segment1_M_max - segment1_M_min), (segment2_M_max-segment2_M_min)) + (K_M/len(union_segment)):
                    #if the segments can be combined, add their union to the segments list
                    if segment1_in_semgents:
                        segments.remove(segment1)
                    if segment2_in_segments:
                        segments.remove(segment2)
                    segments.append(union_segment)
                else:
                    #if the segments remain separate, ensure that they are in the segments list
                    if not segment1_in_semgents:
                        segments.append(segment1)
                    if not segment2_in_segments:
                        segments.append(segment2)
        
        # plotting
        #find each line segment
        for [idx,segment] in enumerate(segments):
            xs = []
            ys = []
            for node in segment:
                xs.append(node.x)
                ys.append(node.y)
            plt.plot(ys,xs,'s',markersize=40)
        #invert the y axis to resemble how image coordinates are stored
        plt.gca().invert_yaxis()
        plt.show()









    def identifier(self, potential_tag):
        '''
        For a potential tag, identify it's fiducial ID or reject it
        '''
        pass
