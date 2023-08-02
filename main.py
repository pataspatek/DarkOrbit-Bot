import cv2 as cv
import numpy as np
import time

from window_capture import WindowCapture
from screen_detector import ScreenDetector
from bot import Bot


def main():
    
    # Initialize the WindowCapture class to capture screenshots from the game window
    wincap = WindowCapture('Dark Orbit')
    screenshot = wincap.get_screenshot()

    # Initialize the ScreenDetector class
    detector = ScreenDetector()

    mini_map_rectangles = detector.find(screenshot, "mini_maps/4-2.png")
    mini_map = mini_map_rectangles[0]

    bot = Bot(mini_map)
    bot.start()

    loop_time = time.time()

    while True:

        # Capture the current screenshot of the game window
        screenshot = wincap.get_screenshot()

        cv.imshow("result", screenshot)

        # Calculate and print the frames per second (FPS) for debugging purposes
        #print(f'FPS: {round((1 / (time.time() - loop_time)), 2)}')
        loop_time = time.time()

        # Check for user input to exit the loop and close the display window
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            bot.stop()
            break


if __name__ == "__main__":
    main()