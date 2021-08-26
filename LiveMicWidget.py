from MicrophoneRecorder import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import numpy as np

class LiveMicWidget(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.fig = plt.Figure(facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()
        mic = MicrophoneRecorder()
        mic.start()

        # computes the parameters that will be used during plotting
        self.time_vect = np.arange(mic.chunksize, dtype=np.float32) / mic.rate * 1000
        self.ax_top = self.fig.add_subplot(111)
        self.ax_top.set_ylim(-32768, 32768)
        self.ax_top.set_xlim(0, self.time_vect.max())
        self.ax_top.set_xlabel(u'time (ms)', fontsize=6)

        # line objects
        self.line_top, = self.ax_top.plot(self.time_vect, np.ones_like(self.time_vect))
        # keeps reference to mic
        self.mic = mic
        self.update_clock()


    def update_clock(self):
        self.handleNewData()
        self.after(1, self.update_clock)


    def handleNewData(self):
        """ handles the asynchroneously collected sound chunks """
        # gets the latest frames
        frames = self.mic.get_frames()
        if len(frames) > 0:
            # keeps only the last frame
            current_frame = frames[-1]
            np.set_printoptions(threshold=sys.maxsize)
            self.line_top.set_data(self.time_vect, current_frame)
            # refreshes the plots
            self.canvas.draw()

