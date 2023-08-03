from threading import Thread, Lock

from vision import Vision


class Detection():

    # Thread properties
    running = False
    lock = None
    rectangles = []

    # Properties
    detector = None
    screenshot = None


    def __init__(self, needle_img_path) -> None:
        
        self.lock = Lock()
        self.detector = Vision()
        self.needle_img_path = needle_img_path
        self.screenshot = None
        self.rectangles = []

        
    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()


    def start(self):
        """
        Start the detection.

        This method sets the running flag to True and starts the detection's main thread.
        """
        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        """
        Stop the detection.

        This method sets the running flag to False, which stops the detection's main loop.
        """
        self.running = False


    def run(self):
        """
        The main loop of the detection.

        This method runs in a separate thread when the detection is started. It will continue to execute until the detection is stopped.
        """
        while self.running:
            if not self.screenshot is None:
                rectangles = self.detector.find(self.screenshot, self.needle_img_path)

                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()
