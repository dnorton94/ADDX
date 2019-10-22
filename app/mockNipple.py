import time
from array import array
import numpy as np
import sys
import re
import glob
import time
import threading
import utils

class MockNipple:
    def __init__(self):
        pass


    def read_scaled(self):
        return utils.shifty_sins()
