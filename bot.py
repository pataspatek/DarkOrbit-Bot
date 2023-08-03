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
    found_objects = None


    def __init__(self, window_size, window_offset, mini_map) -> None:
        """
        Initialize the Bot class.

        :param window_size (tuple): A tuple containing the window size as (width, height).
        :param window_offset (tuple): A tuple containing the window offset as (x, y).
        :param mini_map (tuple): A tuple containing the mini-map position and size as (x, y, width, height).
        """

        # Create a thread lock object
        self.lock = Lock()

        self.window_width = window_size[0]
        self.window_height = window_size[1]

        self.offset_x = window_offset[0]
        self.offset_y = window_offset[1]

        self.mini_map_x = mini_map[0]
        self.mini_map_y = mini_map[1]
        self.mini_map_width = mini_map[2]
        self.mini_map_height = mini_map[3]

        # start bot in the initializing mode to allow us time to get setup.
        self.state = BotState.INITIALIZING
    

    def get_map_coordinates(self):
        
        x = self.mini_map_x
        y = self.mini_map_y
        width = self.mini_map_width
        height = self.mini_map_height

        random_x = random.randint(x, x + width)
        random_y = random.randint(y, y + height)

        return (random_x, random_y)


    def click(self, coordinates):
        screen_x, screen_y = self.get_screen_position(coordinates)
        pyautogui.click(screen_x, screen_y)

    
    def get_screen_position(self, position):
        """
        Convert window coordinates to screen position.

        This method takes individual (x, y) coordinates from the window and converts them into the actual position
        on the screen.

        :param position (tuple): A tuple containing the (x, y) coordinates from the window.
        :return: A tuple containing the screen position as (x, y) coordinates.
        """
        screen_x = position[0] + self.offset_x
        screen_y = position[1] + self.offset_y
        return screen_x, screen_y
    
    
    def stop_movement(self):
        coordinates = ((self.window_width // 2) + 150, self.window_height // 2,)
        self.click(coordinates)


    def collect(self):
        first_rectangle = self.found_objects[0]
        center_x = first_rectangle[0] + (first_rectangle[2] // 2)
        center_y = first_rectangle[1] + (first_rectangle[3] // 2)
        self.click((center_x, center_y))
    

    def update_found_objects(self, objects):
        self.lock.acquire()
        self.found_objects = objects
        self.lock.release()


    def start(self):
        """
        Start the bot.

        This method sets the running flag to True and starts the bot's main thread.
        """
        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        """
        Stop the bot.

        This method sets the running flag to False, which stops the bot's main loop.
        """
        self.running = False
        print("Good Bye")


    def run(self):
        """
        The main loop of the bot.

        This method runs in a separate thread when the bot is started. It will continue to execute until the bot is stopped.
        """
        while self.running:

            # INITIALIZING STATE
            if self.state == BotState.INITIALIZING:
                print("INITIALIZING...")
                time.sleep(5)

                self.lock.acquire()
                self.state = BotState.COLLETING
                self.lock.release()


            elif self.state == BotState.MOVING:
                print("Movement started...")

                coordinates = self.get_map_coordinates()
                self.click(coordinates)

                moving = True

                # Loop until the condition is met or a certain maximum time has elapsed
                max_waiting_time = 5  # Adjust the maximum waiting time as needed
                start_time = time.time()

                while moving:

                    # Check if the maximum waiting time is reached
                    elapsed_time = time.time() - start_time

                    if elapsed_time >= max_waiting_time:
                        break

                    if len(self.found_objects) >= 1:
                        moving = False


                if len(self.found_objects) >= 1:
                    self.lock.acquire()
                    self.state = BotState.COLLETING
                    self.lock.release()

            elif self.state == BotState.COLLETING:

                self.stop_movement()

                while len(self.found_objects) >= 1:
                    self.collect()
                    self.lock.acquire()
                    self.found_objects = self.found_objects[1:]  # Remove the first item from the list
                    self.lock.release()
                    time.sleep(3)

                self.lock.acquire()
                self.state = BotState.MOVING
                self.lock.release()
                