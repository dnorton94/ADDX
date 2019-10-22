import time
import numpy as np

def shifty_sins(f=0.2):
    """
        3 Phase Shifted Sins
    """
    t = time.time()
    pi = np.pi
    theta = 2*pi*f*t

    pitch = 0.5*(1 + np.sin(theta))
    yaw = 0.5*(1 + np.sin(theta - (1/3.0)*2*pi))
    roll = 0.5*(1 + np.sin(theta - (2/3.0)*2*pi))    

    return pitch, yaw, roll