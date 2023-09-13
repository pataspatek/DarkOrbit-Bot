import cv2 as cv
import time

from window_capture import WindowCapture
from bot import Bot
from detection import Detection


def main():
    # Initialize the WindowCapture class to capture screenshots from the game window
    wincap = WindowCapture("Dark Orbit")

    # Initialize the Detection class for bonus box detection
    bonus_box_detection = Detection("bonus_box.png")

    # Initialize the Detection class for mini-map detection
    mini_map_detection = Detection("mini_maps/4-2.png")
    mini_map_rectangles = mini_map_detection.find(wincap.screenshot)
    mini_map = mini_map_rectangles[0]

    # Initialize the Bot with necessary parameters
    bot = Bot(
        window_size=(wincap.window_width, wincap.window_height),
        window_offset=(wincap.offset_x, wincap.offset_y),
        mini_map=mini_map
    )

    # Track the time for FPS calculation
    loop_time = time.time()

    # Start the capture, detection, and bot threads
    wincap.start()
    bonus_box_detection.start()
    bot.start()

    while True:
        # Update bonus box detection with the current screenshot
        bonus_box_detection.update(wincap.screenshot)

        # Update found objects for the bot
        bot.update_found_objects(bonus_box_detection.rectangles)

        # Display the result screen
        cv.imshow("Result", wincap.screenshot)

        # Calculate and print frames per second (FPS) for debugging
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
    """
    Helper function to calculate FPS.
    """
    time_difference = time.time() - loop_time
    if time_difference > 0:  # Avoid division by zero
        fps = 1 / time_difference
        return round(fps, 2)


if __name__ == "__main__":
    main()
