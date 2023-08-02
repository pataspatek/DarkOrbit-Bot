from threading import Thread
import time
import pyautogui


class Bot(): 

    running = False

    move_coordinates = ()


    def __init__(self, window_size, window_offset, mini_map) -> None:

        self.window_width = window_size[0]
        self.window_height = window_size[1]

        self.offset_x = window_offset[0]
        self.offset_y = window_offset[1]
        
        self.mini_map_x = mini_map[0]
        self.mini_map_y = mini_map[1]
        self.mini_map_width = mini_map[2]
        self.mini_map_height = mini_map[3]


    def get_screen_position(self, position):
        """
        Convert window coordinates to screen position.

        This method takes individual (x, y) coordinates from the window and converts them into the actual position on the screen.

        :param position (tuple): A tuple containing the (x, y) coordinates from the window.
        :return: A tuple containing the screen position as (x, y) coordinates.
        """
    
        return (position[0] + self.offset_x, position[1] + self.offset_y)


    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        self.running = False


    def run(self):
        while self.running:
            print(self.mini_map_x)
            print(self.mini_map_y)
            print(self.mini_map_width)
            print(self.mini_map_height)
            time.sleep(5)
