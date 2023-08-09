import cv2 as cv
import numpy as np
import time

from window_capture import WindowCapture
from bot import Bot
from detection import Detection


def main():
    # Initialize the WindowCapture class to capture screenshots from the game window
    wincap = WindowCapture('Dark Orbit')

    # Initialize the Detection class for the bonus box detection
    bonus_box_detection = Detection("bonus_box.png")

    # Initialize the Detection class for the mini map detection
    mini_map_detection = Detection("mini_maps/2-2.png")
    mini_map_rectangles = mini_map_detection.find(wincap.screenshot)
    mini_map = mini_map_rectangles[0]

    bot = Bot(window_size=(wincap.window_width, wincap.window_height),
              window_offset=(wincap.offset_x, wincap.offset_y),
              mini_map=mini_map)

    # Track the time
    loop_time = time.time()

    # Start the threads
    wincap.start()
    bonus_box_detection.start()
    bot.start()

    while True:

        bonus_box_detection.update(wincap.screenshot)

        bot.update_found_objects(bonus_box_detection.rectangles)

        cv.imshow("result", wincap.screenshot)

        # Calculate and print the frames per second (FPS) for debugging purposes
        print(f"FPS: {calculate_fps(loop_time)}")
        loop_time = time.time()

        # Check for user input to exit the loop and close the display window
        key = cv.waitKey(1)
        if key == ord('q'):
            wincap.stop()
            bonus_box_detection.stop()
            bot.stop()
            cv.destroyAllWindows()
            break


def calculate_fps(loop_time):
    time_difference = time.time() - loop_time
    if time_difference > 0:  # Avoid division by zero
        fps = 1 / time_difference
        return round(fps, 2)


if __name__ == "__main__":
    main()
