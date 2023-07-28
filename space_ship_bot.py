import cv2 as cv
import numpy as np
import random

from image_detector import ImageDetector

class SpaceShipBot():

    def __init__(self, method=cv.TM_CCOEFF_NORMED):

        self.method = method


    def get_map_coordinates(self, haystack_img):

        # MAKE SURE THE MINIMAP IN GAME IS OPEN AND THE SMALLEST SIZE
        mini_map = ImageDetector("mini_map.png")

        # List of rectangles containing the locations of matched needle images in a format [x, y, width, height].
        # Should be one match
        rectangles = mini_map.find(haystack_img, threshold=0.4)

        # Get the first rectangle
        map_rectangle = rectangles[0]

        # Sizes of the borders of the map
        left_border = 30
        right_border = 15
        top_border = 50
        bottom_border = 20

        # Adjusted parameters for only clickable part of the mini map
        x = map_rectangle[0] + left_border
        y = map_rectangle[1] + top_border
        width = map_rectangle[2] - left_border - right_border
        height = map_rectangle[3] - top_border - bottom_border

        # Generate coordinates on the mini map
        x = random.randint(x, x + width)
        y = random.randint(y, y + height)
        coordinates = (x, y)

        return coordinates


    def click(self):
        pass




