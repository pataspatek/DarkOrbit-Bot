import cv2 as cv
import numpy as np
import time

from window_capture import WindowCapture
from bot import Bot
from detection import Detection


def main():
    # Initialize the WindowCapture class to capture screenshots from the game window
    wincap = WindowCapture('Dark Orbit')
    screenshot = wincap.get_screenshot()

    # Initialize the bonus box detection
    bonus_box_detection = Detection("bonus_box.png")

    # Found the mini map in order to pass the coordinates to the bot
    mini_map_detection = Detection("mini_maps/2-2.png")
    mini_map_rectangles = mini_map_detection.find(screenshot, "mini_maps/2-2.png")
    mini_map = mini_map_rectangles[0]

    # Initialize the Bot class with the mini-map rectangles
    bot = Bot(window_size=(wincap.window_width, wincap.window_height),
              window_offset=(wincap.offset_x, wincap.offset_y),
              mini_map=mini_map)
    
    # Start each thread
    bot.start()
    wincap.start()
    bonus_box_detection.start()

    # Track the time
    loop_time = time.time()

    while True:

        # Capture the current screenshot of the game window
        screenshot = wincap.get_screenshot()

        # Update the detector with the latest screenshot
        bonus_box_detection.update(screenshot)

        # Update the bot with the detected rectangles
        bot.update_found_objects(bonus_box_detection.rectangles)

        cv.imshow("result", screenshot)

        # Calculate and print the frames per second (FPS) for debugging purposes
        print(f'FPS: {round((1 / (time.time() - loop_time)), 2)}')
        loop_time = time.time()

        # Check for user input to exit the loop and close the display window
        key = cv.waitKey(1)
        if key == ord('q'):
            wincap.stop()
            bonus_box_detection.stop()
            bot.stop()
            cv.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
