import time
import numpy as np
import sys
import argparse
import random
import threading
import serial

import rtmidi_python as rtmidi
import settings as default_settings
import utils
from tracker import Tracker

from serialNippler import SerialNippler

# TODO: Put this in a settings file
PITCH_CC = 86
YAW_CC = 87
ROLL_CC = 88

FRAMERATE = 150

CC_HEX = 0xb0

MODES = [
    "stream",
    "freeze",
    "deep_freeze",
    "stop"
]

class CvStream(threading.Thread):
    """
        Streams non-blocking nipple talk via rtmidi or CV thingy
        Nipple and CV values should be 0->1
        TODO: nipple serial code and cv thingy
    """
    def __init__(self, settings=None, midi_port=None, pitch_cc=PITCH_CC, yaw_cc=YAW_CC, roll_cc=ROLL_CC, framerate=FRAMERATE):
        # Ima thread
        threading.Thread.__init__(self)
        self.daemon=True

        self.serial_nippler = SerialNippler()

        # Setup midi
        self.midi_out = rtmidi.MidiOut(b'in')

        # Default to first port
        if midi_port is None:
            if not self.midi_out.ports:
                raise Exception("No midi ports detected")

            midi_port = self.midi_out.ports[0]

        self.midi_out.open_port(midi_port)

        # Start by streaming
        self.mode = "stream"

        # Control Change is signalled by 0xb0, see: https://www.midi.org/specifications/item/table-1-summary-of-midi-message
        # Also good to stick to typically undefined range, http://nickfever.com/music/midi-cc-list
        self.pitch_cc = pitch_cc
        self.yaw_cc = yaw_cc
        self.roll_cc = roll_cc

        # Safety first
        self.lock = threading.Lock()

        # Default to 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

        self.deep_freeze_pitch = 0
        self.deep_freeze_yaw = 0
        self.deep_freeze_roll = 0

        # Default knobs to full and center
        self.pitch_offset = 0.5
        self.yaw_offset = 0.5
        self.roll_offset = 0.5

        self.pitch_width = 1
        self.yaw_width = 1
        self.roll_width = 1

        self.pitch_mute = False
        self.yaw_mute = False
        self.roll_mute = False

        # Ouput framerate
        self.framerate = framerate

        self.start()

    def set_deep_freeze(self):
        self.deep_freeze_pitch, self.deep_freeze_yaw, self.deep_freeze_roll = [self.pitch, self.yaw, self.roll]

    def set_mode(self, mode):
        """
            Update current mode
        """
        if not mode in MODES:
            raise Exception("Unknown mode %s"%mode)

        self.mode = mode

    def run(self):
        """
            Run meeee
        """
        next_loop = time.time()
        while self.mode != "stop":
            # Sleep to the framerate
            next_loop += 1.0/self.framerate
            time.sleep(max([0, next_loop - time.time()]))

            # Read and write stuff
            with self.lock:
                pitch, yaw, roll = self.read()

                # Read from Serial
                if self.mode == "deep_freeze":
                    self.pitch, self.yaw, self.roll = [self.deep_freeze_pitch, self.deep_freeze_yaw, self.deep_freeze_roll]

                elif self.mode == "freeze":
                    pass
                
                else:
                    self.pitch, self.yaw, self.roll = pitch, yaw, roll

                # Forward downstream
                if self.mode == "stream":
                    # Read from serial                    
                    self.update_midi(self.pitch, self.yaw, self.roll)

                    ######## TODO: Add CV comms here

    def read(self):
        """
            Read from the nipple.
            Returns pitch, yaw, roll
            TODO: Put serial code here
            1Hz schifty sines atm
        """
        ######## TODO: replace this with nipple serial comms
        # pitch, yaw, roll = shifty_sins()
        yaw, pitch, roll = self.serial_nippler.read_scaled()
        ########

        # Rescale wrt width and offset
        return [
            rescale(pitch, self.pitch_offset, self.pitch_width, self.pitch_mute), 
            rescale(yaw, self.yaw_offset, self.yaw_width, self.yaw_mute), 
            rescale(roll, self.roll_offset, self.roll_width, self.roll_mute)
        ]

    def update_midi(self, pitch, yaw, roll):
        """
            Update pitch, yaw and roll
        """
        self.send_midi("pitch", pitch)
        self.send_midi("yaw", yaw)
        self.send_midi("roll", roll)

    def send_midi(self, axis, value):
        """
            axis should be pitch, yaw or roll
        """
        if axis=="pitch":
            cc = self.pitch_cc

        elif axis=="yaw":
            cc = self.yaw_cc

        elif axis=="roll":
            cc = self.roll_cc

        else:
            raise Exception("Unknown axis %s"%axis)

        self.midi_out.send_message([CC_HEX, cc, midi_rescale(value)])

def midi_rescale(value):
    """
        Rescales a value from 0-1 --> 0-127
        Ensures return value is in range and integer
    """
    new_value = value*127

    if new_value < 0:
        new_value = 0
    elif new_value > 127:
        new_value = 127

    return int(new_value)

def rescale(value, offset, width, mute):
    """
        Rescale and rotate [0,1] w.r.t offset and width
        Saturates extremes to [0,1]
    """
    rescaled = offset + (not mute)*width*(value-0.5)
    
    if rescaled<0:
        rescaled = 0

    elif rescaled>1:
        rescaled = 1

    return rescaled

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

def main(args):
    """
        Parsely
    """
    parser = argparse.ArgumentParser(description='Well hello there')
    parser.add_argument('set', nargs='?', choices=["pitch", "yaw", "roll"], help='assign to a parameter in ableton')

    parsed = parser.parse_args(args)

    # Make a Taka-tak-taky-tone
    nipple_handler = NippleHandler()

    # Set param or run
    if parsed.set:
        nipple_handler.send_midi(parsed.set, 0)

    else:        
        nipple_handler.run()
        raw_input("Tell me an anything to stop")

if __name__ == '__main__':    
    main(sys.argv[1:])

