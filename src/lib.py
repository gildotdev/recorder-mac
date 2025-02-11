import os
import sys
import time
from threading import Thread

import cv2
import PIL
import pyautogui
import pyscreeze

__PIL_TUPLE_VERSION = tuple(int(x) for x in PIL.__version__.split("."))
pyscreeze.PIL__version__ = __PIL_TUPLE_VERSION
class lib:
    def __init__(self, delay: float, start_index: int, dir: str, interval: float):
        self.stop = False
        self.allow = True
        self.delay = delay # The delay before taking another screenshot. (Seconds)
        self.index = start_index # The starting index of the image name.
        self.dir = dir # Image Directory Output.
        self.interval = interval # How long to show each frame on video output. (Seconds)
        self.output_repeat = True

    def get_input(self):
        if self.output_repeat:
            print("Press the \'S\' key to stop capturing")
        else: 
            print("Press \'C\' to compile and quit the program. Press \'Q\' to quit the program without compiling.")

        while True:
            get_input = input()
            if not self.stop:
                if get_input == 's': # Check if s is pressed, if True, stop the program from capturing.
                    self.stop = True
                    print("Capture Stopped.")
                    self.output_repeat = False
                    self.get_input()
            else:
                if get_input == 'c': # Check if c is pressed after s, if True, compile all the pictures into a video.
                    self.compile()
                    break
                elif get_input == 'q': # Check if q is pressed after s, if True, quit the program without compiling.
                    sys.exit()

    # Function to generate the picture name.

    def get_filename(self) -> int:
        self.index += 1
        return self.index - 1
    
    # Function to run by a thread to wait after each picture is taken.

    def wait(self):
        self.allow = False
        time.sleep(self.delay)
        self.allow = True

    # Function to capture screenshots until stop is True.
        
    def capture(self):
        while True:
            if not self.stop: # Verify that stop is false.
                if self.allow: # If interval wait time is finished, continue
                    pyautogui.screenshot(self.dir + str(self.get_filename()) + '.png') # Take a screenshot.
                    # print('Captured Screenshot-' + str(self.index))
                    Thread(target=self.wait).start() # Create a interval wait time thread before taking another screenshot.
            else: # If stop is True, output "Capture Ended." and stop the function.
                break

    # Function to compile all the screenshots into a video.

    def compile(self):

        print("Creating video... this may take a couple minutes.")

        # Create a list containing all the image directorys.
        images = [img for img in os.listdir(self.dir) if img.endswith(".png")]
        images_int = [int(img.replace('.png', '')) for img in images]
        images_int.sort()

        list = []

        for i in range(len(images)):
            for j in range(len(images)):
                if (str(images_int[i]) + '.png') == images[j]:
                    list.append(images[j])
            
        images = list
        # Create a frame to get the width and height of the screenshot.
        frame = cv2.imread(os.path.join(self.dir, images[0]))
        height, width, layers = frame.shape

        # Create a VideoWriter to compile the images to a video.
        video = cv2.VideoWriter("../vid/video.mp4", 0, 1 / self.interval, (width,height))

        # Run a for loop to iterate through all the images in a list and write them to the file.
        for image in images:
            video.write(cv2.imread(os.path.join(self.dir, image)))

        # Call the destroyAllWindows() function and release() function.

        cv2.destroyAllWindows()
        video.release()

        print("Video Created Successfully!")

        # Close the program.

        sys.exit()

    # Main function to run.

    def run(self):
        Thread(target=self.get_input).start()
        Thread(target=self.capture).start()
