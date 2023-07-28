import cv2 as cv
import numpy as np
import time

from window_capture import WindowCapture
from image_detector import ImageDetector
from space_ship_bot import SpaceShipBot


def main():
    
    # Initialize the WindowCapture class to capture screenshots from the game window
    wincap = WindowCapture('Dark Orbit')

    # Create an instance of the ImageDetector class for detecting bonus boxes
    bonus_box = ImageDetector("bonus_box.png")

    space_ship = SpaceShipBot()

    loop_time = time.time()


    while True:

        # Capture the current screenshot of the game window
        screenshot = wincap.get_screenshot()

        space_ship.map_move(screenshot)

        # Perform object detection to find bonus boxes in the screenshot
        rectangles = bonus_box.find(screenshot)

        # Draw rectangles around the detected bonus boxes on the original screenshot
        output_img = bonus_box.draw_rectangles(screenshot, rectangles)

        # Display the processed image with detected bonus boxes
        cv.imshow("Mathes", output_img)

        # Calculate and print the frames per second (FPS) for debugging purposes
        print(f'FPS: {round((1 / (time.time() - loop_time)), 2)}')
        loop_time = time.time()

        # Check for user input to exit the loop and close the display window
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


if __name__ == "__main__":
    main()