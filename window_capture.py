import win32gui, win32ui, win32con
import numpy as np
import cv2 as cv

class WindowCapture:

    def __init__(self, window_name=None):
        """
        Initialize the WindowCapture class.

        :param window_name: str, optional
            The name of the window to capture. If None, it captures the entire desktop.
            Default is None.
        """

        # Retrieves a handle to the top-level window whose class name and window name match the specified strings.
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else: 
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception(f'Window not found {window_name}')

        # Returns the rectangle for a window in screen coordinates (left, top, right, bottom)
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.window_width = window_rect[2] - window_rect[0] 
        self.window_height = window_rect[3] - window_rect[1] 

        # Adjust window dimensions and starting position considering borders and title bar
        border_pixels = 8       # Width of the window border in pixels
        titlebar_pixels = 32    # Height of the title bar in pixels

        # Subtract the border pixels twice (for both left and right borders) to get the inner width
        self.window_width = self.window_width - (border_pixels * 2)

        # Subtract the title bar pixels and the border pixels twice (for top border and bottom border) to get the inner height
        self.window_height = self.window_height - titlebar_pixels - (border_pixels * 2)

        # Set the starting position for the window content, considering the border and title bar
        self.starting_x = border_pixels
        self.starting_y = titlebar_pixels

        # Set the cropped coordinates offset so we can translate screenshot images into actual screen positions
        self.offset_x = window_rect[0] + self.starting_x
        self.offset_y = window_rect[1] + self.starting_y


    def get_screenshot(self):
        """
        Capture a screenshot of the specified window.

        :return: numpy.ndarray
            An image array representing the screenshot.
        """

        # Returns the device context (DC) for the entire window, including title bar, menus, and scroll bars. 
        wDC = win32gui.GetWindowDC(self.hwnd)

        # Creates a DC object from an integer handle.
        dcObj = win32ui.CreateDCFromHandle(wDC)
        
        # Creates a memory device context (DC) compatible with the specified device. 
        cDC = dcObj.CreateCompatibleDC()
        
        # Creates a bitmap 
        dataBitMap = win32ui.CreateBitmap()

        # Creates a bitmap compatible with the device that is associated with the specified device context. 
        dataBitMap.CreateCompatibleBitmap(dcObj, self.window_width, self.window_height)

        # Selects an object into the specified device context (DC). The new object replaces the previous object of the same type. 
        cDC.SelectObject(dataBitMap)

        # Performs a bit-block transfer of the color data corresponding to a rectangle of pixels from the specified source device context into a destination device context.
        # Parameters:
            # desPos: from where the pixel displaying starts (typically left top)
            # size: size of the scanned image (width, height)
            # dc: object we want to scan
            # srcPos: from where the scanning starts 
            # rop: raster operation
        cDC.BitBlt((0, 0), (self.window_width, self.window_height) , dcObj, (self.starting_x, self.starting_y), win32con.SRCCOPY)

        # Convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.window_height, self.window_width, 4)

        # Free resources to avoid memory leak
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # Make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img
    

    # Find the name of the window you're interested in.
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)


    def get_screen_position(self, window_coordinats):
        """
        Convert window coordinates to screen position.

        This method takes individual (x, y) coordinates from the window and converts them into the actual position on the screen.

        :param window_coordinates (tuple): A tuple containing the (x, y) coordinates from the window.
        :return: A tuple containing the screen position as (x, y) coordinates.
        """
        
        return (window_coordinats[0] + self.offset_x, window_coordinats[1] + self.offset_y)