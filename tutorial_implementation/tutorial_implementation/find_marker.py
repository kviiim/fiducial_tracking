import enum
from turtle import window_height
import cv2
import numpy as np

class Node():
    def __init__(self, color, D, M):
        """
        color is the color of the pixel in bgr
        D is the range of directions of the gradient
        M in the range of magnitudes of the gradient
        """
        self.D = D
        self.M = M
        self.color = color
        self.edges = {}
    def __repr__(self) -> str:
        print('Node- D: ', self.D, ' M: ', self.M)

class Edge():
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __repr__(self) -> str:
        print('Edge- ', self.weight)

class FindMarker():
    def __init__(self):
        pass

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
                node = Node(pixel, D, M)
                print('node', idx, pixel, D, M)
                image_nodes[idx] = node

                current_node = image_nodes[idx]
                if x != 0: 
                    # if x is not zero we can find the left pixel
                    left_node = image_nodes[idx - 1]
                    left_node.edges[current_node] = abs(current_node.D - left_node.D)
                    edges = np.append(edges, Edge(left_node, current_node, abs(current_node.D - left_node.D)))

                if y != 0:
                    # if y is not zero we can find the top pixel
                    top_node = image_nodes[idx - len(row)]
                    top_node.edges[current_node] = abs(current_node.D - top_node.D)
                    edges = np.append(edges, Edge(top_node, current_node, abs(current_node.D - top_node.D)))

                # if neither is zero we can find the diagonal left pixel 
                if x != 0 & y != 0:
                    top_left = image_nodes[idx - len(row) - 1]
                    top_left.edges[current_node] = abs(current_node.D - top_left.D)
                    edges = np.append(edges, Edge(top_left, current_node, abs(current_node.D - top_left.D)))

        edges = sorted(edges, key=lambda edge : edge.weight)
        for edge in edges:
            # need to fix this
            #find segment for node 1
            if edge.node1 in segments:
                #this should become the segment
                segment1 = 0
            else:
                segment1 = {edge.node1}
            #find segment for node 2
            if edge.node2 in segments:
                #this should become the segment
                segment2 = 0
            else:
                segment2 = {edge.node2}

            union_segment = segment1.union(segment2)
            





    def identifier(self, potential_tag):
        '''
        For a potential tag, identify it's fiducial ID or reject it
        '''
        pass
