import serial
import time
from array import array
import numpy as np

import re
import glob
import sys
import random
import utils
import time
CV_BAUD = 19200

class SerialCv:
    def __init__(self):
        # Detect Nipple port
        # TODO: DRY with serialNippler
        cv_ports = glob.glob('/dev/cu.usbmodem*')
        if (len(cv_ports)!=1):
            raise Exception("Found %i cv ports, expected one"%len(cv_ports))

        self.port = cv_ports[0]
        self.serial = serial.Serial(port=cv_ports[0], baudrate=CV_BAUD)     

    def write(self, pitch, yaw, roll):
        """
            Accepts numbers 0->1
        """
        split = []
        
        numList = [
            'cvall',
            serialise(pitch),
            serialise(yaw),
            serialise(roll),
        '0\n']

        self.serial.write((','.join(numList)).encode("utf-8"))

def serialise(val):
    rescaled = int(val*255)

    if rescaled<0:
        rescaled = 0

    elif rescaled>255:
        rescaled=255

    return str(rescaled)

if __name__ == "__main__":
    serial_cv = SerialCv()
    framerate = 150

    start_time = time.time()
    next_time = time.time() + 1.0/framerate
    print("Streaming schifty sins")
    while True:
        t_start = time.time()
        serial_cv.write(*utils.shifty_sins())

        time.sleep(max([0, next_time-time.time()]))
        next_time += 1.0/framerate
        print("framerate %.0f"%(1.0/(time.time()-t_start)))
        print("elapsed %.0fs"%(time.time()-start_time))
