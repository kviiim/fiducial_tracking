import enum
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

class FindMarker():
    def __init__(self):
        pass

    def detector(self, image):
        '''
        Identify tag shaped items in a given image
        '''
        #create image graph
        segmentation_graph = np.zeros(image.shape[0], image.shape[1])
        #process each pixel
        for [y,row] in enumerate(image):
            for [x,pixel] in enumerate(row):
                #calculate gradient of pixel            
                x_grad = image[y][x+1] - image[y][x-1]
                y_grad = image[y+1][x] - image[y-1][x]

                #calculate direction and magnitude of gradient
                D = np.arctan2(y_grad/x_grad)
                M = np.sqrt(x_grad**2 + y_grad**2)

                #create pixel node in graph
                segmentation_graph[row][pixel] = Node(pixel, D, M)

        #once each gradient is calculated, find edges
        for [row_idx, row] in enumerate(segmentation_graph):
            for [col_idx, n] in enumerate(row):
                #if we are at the image edge don't check for new graph edges
                if col_idx == len(row) - 1 or row_idx == len(segmentation_graph) - 1:
                    pass
                for m_col_delta in range(2):
                    for m_row_delta in range(2):
                        m = segmentation_graph[row_idx + m_row_delta][col_idx + m_col_delta]


    def identifier(self, potential_tag):
        '''
        For a potential tag, identify it's fiducial ID or reject it
        '''
        pass
