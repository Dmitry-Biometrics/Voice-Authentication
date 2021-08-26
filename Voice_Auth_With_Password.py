import tkinter as tk  # Python 3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import os
import wave
from tkinter import ttk
from PIL import ImageTk, Image
import sys
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar
import pygame
import shutil
import math
from RecordingFile import *
from LiveMicWidget import *
from LeftMainForm import *
from RightMainForm import *
from speech_to_text import *
from center import *
from pydub import AudioSegment, effects
import time


class voice_auth(tk.Frame):
    def __init__(self, master=None):
        if not os.path.exists("model"):
            tk.messagebox.showerror("Error", "Missing model")
            print(
                "Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder.")
        self.speach_to_text = SpeachToText(model_for_recog,"")
        tk.Frame.__init__(self, master)
        menubar = tk.Menu(main_root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=main_root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        main_root.config(menu=menubar)
        main_root.minsize(width=1350, height=900)

        # все что в правой части макете
        rightform = tk.Frame(master=main_root, bd=2, width=350, height=800, relief=tk.SUNKEN)
        rightform.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Список образов и скролбар
        self.mylist = tk.Listbox(rightform, height=27, highlightcolor="red", font=("Ariel", "16"))
        self.right_form_c = RightForm(rightform, model_for_recog, self.mylist)

        # все что в левой части макете
        leftform = tk.Frame(master=main_root, bd=2, width=600, height=800, relief=tk.GROOVE)
        leftform.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        LeftForm(leftform, model_for_recog,self.mylist)

        main_root.grid_columnconfigure(0, weight=1)
        main_root.grid_rowconfigure(0, weight=1)

        # Кнопка Старт/Стоп
        self.button1_was_clicked = False
        self.recording_started = False
        self.recording_stopped = False
        self.btn_start = tk.Button(master=main_root, text="Burn image", bg="green", font="85",
                                   image=btn_record_image,
                                   compound=tk.LEFT, command=self.buttonClickedRecord)
        self.btn_start.pack(side=tk.BOTTOM)


        # Экран снятия сигнала
        LiveMicWidget(master=main_root)


    def ShowImage(self, event):
        pass

    def match_target_amplitude(self, sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def buttonClickedRecord(self):
        was_start = False
        if self.btn_start["text"] == "Burn image" and not self.recording_started:
            self.recording_file = RecordingFile(fname = os.getcwd() +"\output.wav",
                                                mode='wb',
                                                channels=1,
                                                rate=16000,
                                                frames_per_buffer=1024)
            self.recording_file.start_recording()
            self.recording_started = True
            self.button1_was_clicked = True
            self.btn_start.config(text="Stop recording")
            self.btn_start.config(bg = "red")
            was_start = True

        if  self.btn_start["text"] == "Stop recording" and self.recording_started and not was_start:
            self.recording_file.stop_recording()
            self.recording_started = False
            self.recording_stopped = True
            #Finished recording, normalized by height
            sound = AudioSegment.from_file(os.getcwd() +"\output.wav", "wav")
            normalized_sound = self.match_target_amplitude(sound, -20.0)
            normalized_sound.export(os.getcwd() +"\output.wav", format="wav")
            self.right_form_c.save_rezults()
            self.btn_start.config(text="Burn image")
            self.btn_start.config(bg="green")


if __name__ == '__main__':
    main_root = tk.Tk()
    main_root.attributes('-alpha', 0.0)
    main_root.title("Biometric Password Voice Authentication")
    global btn_record_image
    btn_record_image = tk.PhotoImage(file=os.getcwd() + "\\res\\record.png")
    #Initializing the model
    model_for_recog = Model("model")
    voice_auth(master=main_root)
    center(main_root)
    main_root.attributes('-alpha', 1.0)
    main_root.mainloop()
