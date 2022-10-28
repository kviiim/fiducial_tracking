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

class Edge():
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __repr__(self) -> str:
        print(self.weight)

class FindMarker():
    def __init__(self):
        pass

    def detector(self, image):
        '''
        Identify tag shaped items in a given image
        '''
        #create image graph
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale', image)
        print("grayscale size", image.shape)
        segmentation_graph = np.zeros(image.shape[0] * image.shape[1], dtype=Node)
        edges = np.array([], dtype=Edge)
        # create a set of components
        components = set()
        #process each pixel
        for [y,row] in enumerate(image):
            for [x,pixel] in enumerate(row):
                print(x, y)
                #calculate gradient of pixel
                if x != len(row) -1 | x != 0:
                    x_grad = image[y][x+1] - image[y][x-1]
                else: 
                    # TODO: Fix this
                    x_grad = 0.1
                if y != len(image) -1 | y != 0:
                    y_grad = image[y+1][x] - image[y-1][x]
                else:
                    # TODO: Fix this
                    y_grad = 0.1
                print('xgrad', x_grad, 'ygrad', y_grad)
                #calculate direction and magnitude of gradient
                D = np.arctan2(y_grad, x_grad)
                M = np.sqrt(x_grad**2 + y_grad**2)

                idx = y * len(row) + x
                #create pixel node in graph
                segmentation_graph[idx] = Node(pixel, D, M)

                current_node = segmentation_graph[idx]
                if x != 0: 
                    # if x is not zero we can find the left pixel
                    left_node = segmentation_graph[idx - 1]
                    left_node.edges[current_node] = abs(current_node.D - left_node.D)
                    edges = np.append(edges, Edge(left_node, current_node, abs(current_node.D - left_node.D)))

                if y != 0:
                    # if y is not zero we can find the top pixel
                    top_node = segmentation_graph[idx - len(row)]
                    top_node.edges[current_node] = abs(current_node.D - top_node.D)
                    edges = np.append(edges, Edge(top_node, current_node, abs(current_node.D - top_node.D)))

                # if neither is zero we can find the diagonal left pixel 
                if x != 0 & y != 0:
                    top_left = segmentation_graph[idx - len(row) - 1]
                    top_left.edges[current_node] = abs(current_node.D - top_left.D)
                    edges = np.append(edges, Edge(top_left, current_node, abs(current_node.D - top_left.D)))
        print(edges)
        edges = sorted(edges, key=lambda edge : edge.weight)
        print(edges)

    def identifier(self, potential_tag):
        '''
        For a potential tag, identify it's fiducial ID or reject it
        '''
        pass
