import serial
import time
from array import array
import numpy as np
import sys
import re
import glob
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

NIPPLE_BAUD = 115200
TOLERANCE = 0.005 # For calibration
# TOLERANCE = 0.5 # For calibration
RANGE = 10

class SerialNippler:
    def __init__(self, val_range=RANGE):
        # Detect Nipple port
        nipple_ports = glob.glob('/dev/cu.wch*')
        if (len(nipple_ports)!=1):
            raise Exception("Found %i nipple ports, expected one"%len(nipple_ports))

        self.port = nipple_ports[0]
        self.serial = serial.Serial(port=nipple_ports[0], baudrate=NIPPLE_BAUD)     

        self.center = self.calibrate()

    def read(self):
        split = []
        while True:
            self.serial.write(b'a') # send byte to Arduino
            received_data = str(self.serial.readline())
            
            split = received_data.split(",") # split data

            # HACK: to cover up an unstable nipple
            if len(split) != 5:
                continue

            try:
                x = float(split[1])
                y = float(split[2])
                z = float(split[3])

                break

            except Exception as e:
                split = []

        return np.array([x,y,z]).astype(float)

    def read_scaled(self, scale_size=RANGE):
        """
        """
        scale_size = float(scale_size)

        # Scale it
        scaled_reading = 0.5 + (self.read() - self.center)/float(scale_size)

        scaled_reading[scaled_reading<0] = 0                
        scaled_reading[scaled_reading>1] = 1

        return scaled_reading

    def calibrate(self, samples_per_reading=50):
        """
            Return when calibrated
        """
        calibrated = False
        while not calibrated:
            reading0 = self.read()

            for i in range(samples_per_reading):
                reading1 = self.read()

            # Take a diff
            error = np.max(np.abs(reading0-reading1))

            # Check tolerance
            calibrated = error<TOLERANCE

            if error != 0:
                print("%.0f%% calibrated"%(100*TOLERANCE/error))

        return reading1

def within_tolerance(x,y, tol):
    """
        Returns True or the how far away it is
    """
    return abs(x-y)<tol

animation_readings = []
animation_times = []
framerates = []
t_start = time.time()
time_window = 10
t_prev = t_start-1
def animate(i, ax, serial_nippler):
    global animation_readings
    global animation_times
    global framerates
    global t_prev
    global reading
    ax.clear()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("")

    framerate = 1.0/(time.time()-t_prev)
    t_prev = time.time()
    framerates.append(framerate)

    t_start_read = time.time()
    animation_readings.append(reading)

    legends = ["pitch", "yaw", "roll"]
    
    animation_times.append(t_prev) 

    idx = np.argmax(np.array(animation_times)>=(animation_times[-1]-time_window))
    animation_readings = animation_readings[idx:]
    animation_times = animation_times[idx:]
    readings_np = np.array(animation_readings)
    framerates = framerates[idx:]

    ax.plot(animation_times, framerates, label="framerate")

    for i in range(readings_np.shape[1]):
        ax.plot(animation_times, readings_np[:,i], label=legends[i])

    for y0 in serial_nippler.center:
        ax.axhline(y=y0, linestyle=":")

    if len(animation_times)>2:
        ax.set_xlim([animation_times[0],animation_times[-1]])
    
    ax.legend()


def hackyReadThread(serial_nippler):
    global reading

    read_times = []
    while True:
        read_times.append(time.time())
        print("Framerate", 1.0/(np.mean(np.diff(read_times))))
        reading = serial_nippler.read()


if __name__ == "__main__":

    serial_nippler = SerialNippler()

    reading = serial_nippler.read()
    thread = threading.Thread(target=hackyReadThread, args=(serial_nippler,))
    thread.daemon = True
    thread.start()

    max_diff = 0

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)


    ani = animation.FuncAnimation(fig, 
        lambda i: animate(i, ax, serial_nippler), 
        interval=1000/50
    )
    plt.show()

    quit()

    while True:
        max_reading_diff = np.max(serial_nippler.read() - serial_nippler.center)
        if max_reading_diff > max_diff:
            max_diff = max_reading_diff

        print('Max Diff: %.5f\r'%max_diff)
        print('read', serial_nippler.read() - serial_nippler.center)
        print('read scaled', serial_nippler.read_scaled())
        # sys.stdout.flush()

    quit()


    def wait_for_calibration(xold, yold, zold, xnew, ynew, znew, epsilon, *args, **kwargs):
        # calibration algorithm, find whether x,y,z values converge
        if (abs(xold - xnew) < epsilon and abs(yold - ynew) < epsilon and abs(zold - znew) < epsilon):
            calib = True
        else:
            calib = False
        return calib

    print("serial set up")


    n = 0 # number of data lines received

    xold = 0 # old value of x
    yold = 0 # old value of x
    zold = 0 # old value of x

    calib=False
    while True:
        ser.write(b'a') # send byte to Arduino
        received_data = str(ser.readline())
        split = received_data.split(",") # split data
        n += 1

        if len(split) == 5: # check whether length is correct
            # convert values to float
            x = float(split[1]) 
            y = float(split[2])
            z = float(split[3])

            if calib == False:
                calib = calibrated(xold, yold, zold, x, y, z, TOLERANCE) # call calibration algorithm
                if n == 50: # update values at every 50th datapoint, without this the calibration ends before x,y,z are convergent
                    xold = x
                    yold = y
                    zold = z
                    n = 0
            else:
                # calculate integer values
                x_send = int( 124 + (x - xold) * 10)
                y_send = int( 124 + (y - yold) * 10)
                z_send = int( 124 + (z - zold) * 10)

                # thresholding 
                if x_send > 255:
                    x_send = 255
                if y_send > 255:
                    y_send = 255
                if z_send > 255:
                    z_send = 255
                if x_send < 0:
                    x_send = 0
                if y_send < 0:
                    y_send = 0
                if z_send < 0:
                    z_send = 0

                print(x_send, y_send, z_send)

                numList = ['cvall',str(x_send) , str(y_send), str(z_send), '0\n']
                seperator = ','

                serCV.write((seperator.join(numList)).encode("utf-8"))
