from threading import Thread, Lock
import cv2 as cv
import numpy as np
import time


class Detection():

    # Thread properties
    running = False
    lock = None
    rectangles = []

    # Properties
    screenshot = None


    def __init__(self, needle_img_path) -> None:
        
        # Initialize the state of the running thread to False
        self.running = False

        # Create a thread lock object
        self.lock = Lock()
        
        # Path to the image for detection
        self.needle_img_path = needle_img_path

        # Haystack image in which the image is detected
        self.screenshot = None

        # Rectangles of the found images
        self.rectangles = []


    def find(self, haystack_img, threshold=0.75, method=cv.TM_CCOEFF_NORMED):
        """
        Find the needle images in the haystack image using template matching.

        :param haystack_img: The image in which the needle image will be searched.
        :param threshold: Similarity threshold for template matching (default: 0.75).
        :param method: Method to use for template matching (default: cv.TM_CCOEFF_NORMED).
        :return: List of rectangles containing the locations of matched needle images in the format [x, y, width, height].
        """

        # Read the needle image
        self.needle_img = cv.imread(self.needle_img_path, cv.IMREAD_UNCHANGED)

        # Get the width and the height of the needle image
        needle_img_height = self.needle_img.shape[0]
        needle_img_width = self.needle_img.shape[1]

        # Find needle img in the haystack img
        result = cv.matchTemplate(haystack_img, self.needle_img, method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)

        # Create a list of x, y coordinates
        locations = list(zip(*locations[::-1]))

        # Create a list of [x, y width, height] rectangles
        rectangles = []
        for loc in locations:
            rectangle = [int(loc[0]), int(loc[1]), needle_img_width, needle_img_height]
            rectangles.append(rectangle)

        # Group similar rectangles to remove duplicate detections and overlapping regions.
        rectangles, _ = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles
    
    
    def get_center_point(self, rectangles):    
        """
        Get the center points of the rectangles.

        :param rectangles: List of rectangles in the format [x, y, width, height].
        :return: List of center points as (x, y) tuples.
        """

        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                # Save the points
                points.append((center_x, center_y))

        return points
    

    def draw_rectangles(self, haystack_img, rectangles):
        """
        Draw rectangles on the haystack image.

        :param haystack_img: The image on which rectangles will be drawn.
        :param rectangles: List of rectangles in the format [x, y, width, height].
        :return: The haystack image with drawn rectangles.
        """
                    
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
                
        for (x, y, w, h) in rectangles:
            
            # Determine the box position
            top_left = (x, y)
            bottom_right = (x + w, y + h)

            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, lineType=line_type)
            
        return haystack_img
    

    def draw_crosshairs(self, haystack_img, points):
        """
        Draw crosshairs (markers) on the haystack image at specified points.

        :param haystack_img: The image on which crosshairs will be drawn.
        :param points: List of points as (x, y) tuples.
        :return: The haystack image with drawn crosshairs.
        """
    
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for center_x, center_y in points:
                    
            # Draw the center point
            cv.drawMarker(haystack_img, (center_x, center_y), color=marker_color, markerType=marker_type)

        return haystack_img

        
    def update(self, screenshot):
        """
        Update the screenshot for detection.

        :param screenshot: Haystack image in which the objects are detected.
        """

        # Lock the thread while updating the properties
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()


    def start(self):
        """
        Start the detection.
        """

        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        """
        Stop the detection.
        """

        self.running = False


    def run(self):
        """
        The main loop of the detection.

        This method runs in a separate thread when the detection is started. It will continue to execute until the detection is stopped.
        """
        
        while self.running:
            if not self.screenshot is None:
                rectangles = self.find(self.screenshot)

                # Lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()
