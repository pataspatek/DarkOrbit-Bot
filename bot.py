from threading import Thread, Lock
import time
import pyautogui
import random


class BotState():

    INITIALIZING = 0
    MOVING = 1
    COLLETING = 2


class Bot():

    # Thread properties
    running = False
    lock = None

    # Bot properties
    state = None
    found_objects = []


    def __init__(self, window_size, window_offset, mini_map) -> None:
        """
        Initialize the Bot class.

        :param window_size: Tuple containing the window size as (width, height).
        :param window_offset: Tuple containing the window offset as (x, y).
        :param mini_map: Tuple containing the mini-map position and size as (x, y, width, height).
        """

        # Create a thread lock object
        self.lock = Lock()

        # Retrieve window width and height 
        self.window_width = window_size[0]
        self.window_height = window_size[1]

        # Retrieve windows offsets
        self.offset_x = window_offset[0]
        self.offset_y = window_offset[1]

        # Retrieve mini map parameters
        self.mini_map_x = mini_map[0]
        self.mini_map_y = mini_map[1]
        self.mini_map_width = mini_map[2]
        self.mini_map_height = mini_map[3]

        # start bot in the initializing mode to allow us time to get setup.
        self.state = BotState.INITIALIZING
    

    def get_random_map_coordinates(self):
        """
        Generate random coordinates on the mini-map for movement.

        :return: Tuple (x, y)
        """
        
        x = self.mini_map_x
        y = self.mini_map_y
        width = self.mini_map_width
        height = self.mini_map_height

        random_x = random.randint(x, x + width)
        random_y = random.randint(y, y + height)

        return (random_x, random_y)


    def click(self, coordinates):
        """
        Perform a mouse click at the specified coordinates.

        :param coordinates: Tuple (x, y) representing the coordinates to click.
        """

        screen_x, screen_y = self.get_screen_position(coordinates)
        pyautogui.click(screen_x, screen_y)

    
    def get_screen_position(self, position):
        """
        Convert window coordinates to screen position.

        :param position: Tuple containing the (x, y) coordinates from the window.
        :return: Tuple containing the screen position as (x, y) coordinates.
        """

        screen_x = position[0] + self.offset_x
        screen_y = position[1] + self.offset_y
        return screen_x, screen_y
    

    def get_center_of_first_object(self):
        """
        Get the center coordinates of the first found object for collecting.

        :return: Tuple (x, y) representing the center coordinates.
        """

        first_rectangle = self.found_objects[0]
        center_x = first_rectangle[0] + (first_rectangle[2] // 2)
        center_y = first_rectangle[1] + (first_rectangle[3] // 2)
        return center_x, center_y


    def update_found_objects(self, objects):
        """
        Update the list of found objects.
        :param objects: List of objects found by detection.
        """

        self.lock.acquire()
        self.found_objects = objects
        self.lock.release()


    def start(self):
        """
        Start the bot.
        """

        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        """
        Stop the bot.
        """

        self.running = False
        print("Good Bye")


    def run(self):
        """
        The main loop of the bot.

        This method runs in a separate thread when the bot is started.
        """
        
        while self.running:

            # Initializing state
            if self.state == BotState.INITIALIZING:
                print("Initializing...")
                time.sleep(5)

                # Lock the thread while updating the results
                self.lock.acquire()
                self.state = BotState.COLLETING
                self.lock.release()

            # Moving state
            elif self.state == BotState.MOVING:
                print("Moving...")

                coordinates = self.get_random_map_coordinates()
                self.click(coordinates)

                # Loop until the condition is met or a certain maximum time has elapsed
                max_waiting_time = 8  # Adjust the maximum waiting time as needed
                start_time = time.time()

                while True:

                    # Check if the maximum waiting time is reached
                    elapsed_time = time.time() - start_time

                    if elapsed_time >= max_waiting_time:
                        break

                    if len(self.found_objects) >= 1:
                        break


                if len(self.found_objects) >= 1:
                    # Lock the thread while updating the results
                    self.lock.acquire()
                    self.state = BotState.COLLETING
                    self.lock.release()

            # Collecting state
            elif self.state == BotState.COLLETING:
                print("Collecting")

                while len(self.found_objects) > 0:
                    item_coordinates = self.get_center_of_first_object()
                    self.click(item_coordinates)
                    time.sleep(2)

                # Lock the thread while updating the results
                self.lock.acquire()
                self.state = BotState.MOVING
                self.lock.release()