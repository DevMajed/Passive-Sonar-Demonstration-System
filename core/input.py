import sounddevice as sd
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# For handling debug output
import logging

# For getting size of sample in bytes
import sys

# For measuring current time
import time as time_module

# local import of localization code
from core.localization import Localization

class UserInputStream(sd.InputStream):
    """
    Class that handles the storing of audio input data.
    """
    def __init__(self, sampleRate, debug):
        # call sd.InputStream initialization
        # Try to open Virtual Audio Cable input device. If the Virtual Cable is not active, then initiate the
        # sounddevice input stream with default device
        try:
            super().__init__(samplerate=sampleRate, device="Line 1 (Virtual Audio Cable), Windows WASAPI",
                             channels=2, dtype=np.int16, callback=self.inputCallback, latency="low")
        except ValueError:
            super().__init__(samplerate=sampleRate, channels=2, dtype=np.int16, callback=self.inputCallback, latency="low")

        self.localization = Localization(sampleRate)    # initialize Localization object using project sample rate
        
        self.sampleRate = sampleRate
        self.debug = debug

        # initialize values used for input callback
        self.currentTime = 0
        #self.timeDifference = 0
        self.time_x = None
        self.numSamples = None
        # self.time_x = np.linspace(0.0, 0.1, 480)

        # initial amplitude values
        self.l = None
        self.r = None

        # used for setting up plot
        self.fig = plt.figure()
        # self.ax = plt.axes(xlim=(0, 4), ylim=(-2, 2))
        self.ax = plt.axes()
        self.line, = self.ax.plot([], [], lw=3)

        # anim = FuncAnimation(self.fig, self.animateFrame, init_func=self.initPlot, interval=20, blit=True)

    def inputCallback(self, indata, frames, time, status):
        """
        Called by stream periodically, automatically
        """

        if self.debug["time_localization"]:
            start = time_module.time()

        self.numSamples = indata.shape[0]
        self.timeDifference = time.currentTime - self.currentTime
        self.currentTime = time.currentTime
        self.time_x = np.linspace(0.0, self.timeDifference, self.numSamples)

        self.l = [channel[0] for channel in indata]
        self.r = [channel[1] for channel in indata]

        if self.debug["samples"]:
            logging.info(indata.shape[0])
        if self.debug["amplitude"]:
            logging.info(indata)
        if self.debug["bytes"]:
            # logging.info(indata[0][0])
            logging.info(self.dtype)
            # logging.info(sys.getsizeof(indata[0][0]))   # type: numpy mdarray
        if self.debug["time_processing"]:
            logging.info("processing time: {0} ms".format((time.inputBufferAdcTime - time.currentTime) * 1000))

        ######### localization #########
        self.localization.runLocalization(self.l, self.r)   # results stored to self.localization instance

        if self.debug["time_localization"]:
            logging.info("processing + localization time: {0} ms".format((time.inputBufferAdcTime - time.currentTime + time_module.time() - start) * 1000))