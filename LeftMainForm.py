import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
import math
import wave
from speech_to_text import *
from Biometric_params import *
from center import *
from bio_params_view import *
from net_training import *

class LeftForm(tk.Frame):
    def __init__(self, master,model, train_list):
        tk.Frame.__init__(self, master)
        self.model_for_recog = model
        self.mylist = train_list
        global wav_logo
        wav_logo = tk.PhotoImage(file=os.getcwd() + "\\res\\wav_logo.png")
        global voice_params_image
        voice_params_image = tk.PhotoImage(file=os.getcwd() + "\\res\\bio_params.png")
        global btn_train_image
        btn_train_image = tk.PhotoImage(file=os.getcwd() + "\\res\\neuron.png")
        # Button Display wav.forms of all images
        self.btn_get_wav_params = tk.Button(master=master, text="Withdraw \n .wav forms of \n images ",
                                            image=wav_logo, bg="medium aquamarine",
                                            command=self.buttonClickedGetWav, font="18", compound=tk.LEFT)
        self.btn_get_wav_params.pack(padx=10, pady=80)

        # Button Display biometrics
        Bioview = get_bio_params_view()

        self.btn_get_bio_params = tk.Button(master=master, text="Biometric \n parameters",
                                            image=voice_params_image, bg="medium aquamarine",
                                            command=Bioview.buttonClickedGetBio, font="18", compound=tk.LEFT)
        self.btn_get_bio_params.pack(padx=10, pady=40)

        # Teach Network button
        TrainingNet = NetTrain(model, self.mylist)
        self.btn_train = tk.Button(master=master, text="      Train the network          ", image=btn_train_image,
                                   bg="medium aquamarine",
                                   command=TrainingNet.buttonClickedTrain, font="18", compound=tk.LEFT)
        self.btn_train.pack(padx=10, pady=60)


    def buttonClickedGetWav(self):
        self.newWindowAllwav = tk.Toplevel()
        self.newWindowAllwav.title("Wav form images")
        self.newWindowAllwav.focus_set()
        menubar2 = tk.Menu(self.newWindowAllwav)
        filemenu2 = tk.Menu(menubar2, tearoff=2)
        filemenu2.add_command(label="Close", command=self.newWindowAllwav.destroy)
        filemenu2.add_command(label="On one graph", command=self.OnOneGraph)
        menubar2.add_cascade(label="View", menu=filemenu2)
        self.newWindowAllwav.config(menu=menubar2)
        filelist = [f for f in os.listdir("Images")]
        rowq = 0
        columnq = 0

        for f in filelist:
            if f.endswith(".wav"):
                if columnq == 4:
                    columnq = 0
                    rowq += 1
                path = "Images/" + f
                spf = wave.open(path, "r")
                signal = spf.readframes(-1)
                signal = np.frombuffer(signal, dtype='int16')
                self.add_wav_image(path, rowq,columnq, f, signal)
                columnq += 1
        center(self.newWindowAllwav)
        self.newWindowAllwav.mainloop()

    def OnOneGraph(self):
        self.newWindowWav = tk.Toplevel()
        self.newWindowWav.title("Wav form images")
        self.newWindowWav.focus_set()
        self.newWindowWav.minsize(width=1050, height=800)

        menubar2 = tk.Menu(self.newWindowWav)
        filemenu2 = tk.Menu(menubar2, tearoff=2)
        filemenu2.add_command(label="Close", command=self.newWindowWav.destroy)
        filemenu2.add_command(label="On one graph", command=self.OnOneGraph)
        menubar2.add_cascade(label="View", menu=filemenu2)
        self.newWindowWav.config(menu=menubar2)
        filelist = [f for f in os.listdir("Images")]
        fig = plt.Figure(facecolor='white', figsize=(4, 3.5), dpi=80)
        canvas = FigureCanvasTkAgg(fig, master=self.newWindowWav)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        max_x = 0
        min_y = 0
        max_y = 0
        for f in filelist:
            if f.endswith(".wav"):
                path = "Images/" + f
                spf = wave.open(path, "r")
                signal = spf.readframes(-1)
                signal = np.frombuffer(signal, dtype='int16')
                if signal.min() < min_y:
                    min_y = signal.min()
                if signal.max() > max_y:
                    max_y = signal.max()
                if len(signal) > max_x:
                    max_x = len(signal)
        for f in filelist:
            if f.endswith(".wav"):
                path = "Images/" + f
                spf = wave.open(path, "r")
                signal = spf.readframes(-1)
                signal = np.frombuffer(signal, dtype='int16')
                time_vect = np.arange(max_x, dtype=np.float32) / 4000 * 1000
                curent_x = len(signal)
                for i in range (max_x - curent_x):
                    signal = np.append(signal,0)

                ax_top = fig.add_subplot(111)
                ax_top.set_ylim(min_y, max_y)
                ax_top.set_xlim(0, len(signal) / 4)
                line_top, = ax_top.plot(time_vect, np.ones_like(time_vect))
                line_top.set_data(time_vect, signal)
                canvas.draw()
        center(self.newWindowWav)
        self.newWindowWav.mainloop()

    def add_wav_image(self, path, rowq, columnq, name, signal):
        fig = plt.Figure(facecolor='white',figsize=(4, 3.5), dpi=80)
        canvas = FigureCanvasTkAgg(fig, master=self.newWindowAllwav)
        canvas.get_tk_widget().grid(row=rowq, column=columnq)
        time_vect = np.arange(len(signal), dtype=np.float32) / 4000 * 1000
        ax_top = fig.add_subplot(111)
        ax_top.set_ylim(signal.min(), signal.max())
        ax_top.set_xlim(0, len(signal) / 4)
        ax_top.set_xlabel(name, fontsize=6)
        line_top, = ax_top.plot(time_vect, np.ones_like(time_vect))
        line_top.set_data(time_vect, signal)
        canvas.draw()