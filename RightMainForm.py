import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
import math
import wave
import seaborn as sns
import re
from Voice_Auth_With_Password import *
from speech_to_text import *
from Biometric_params import *
from center import *


class RightForm(tk.Frame):
    def __init__(self, master, model,train_list):
        tk.Frame.__init__(self, master)
        self.model_for_recog = model
        self.current_path =""
        self.current_value = "Image №1"
        self.mylist = train_list

        global play_image
        play_image = tk.PhotoImage(file=os.getcwd() +"\\res\\play.png")
        global stop_image
        stop_image = tk.PhotoImage(file=os.getcwd() +"\\res\\stop.png")

        self.mylist.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S),)
        s = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.mylist.yview)
        s.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self.mylist['yscrollcommand'] = s.set
        for file in os.listdir("Images"):
            if file.endswith(".wav"):
                self.mylist.insert(tk.END, file[:-4])

        self.mylist.select_set(0)
        self.mylist.focus_set()

        self.mylist.bind('<<ListboxSelect>>', self.list_to_entry)
        self.mylist.bind('<Button-3>', self.rClicker, add='')
        self.current_selection = (0,)
        self.mylist.select_set(self.current_selection)
        self.mylist.focus_set()


        # Delete All button
        self.delete_all_images = tk.Button(master=master, text="          clear the list", bg="medium aquamarine",
                                           command=self.buttonClickedDeleteAllImages, font="18",
                                           anchor=(tk.W)).grid(column=0, columnspan=2, row=1, pady=20,
                                                               sticky=(tk.W, tk.E))

        # Upload Images button
        self.add_images = tk.Button(master=master, text="          Add images", bg="medium aquamarine",
                                    command=self.buttonClickedAddImages, font="18",
                                    anchor=(tk.W)).grid(column=0, columnspan=2, row=2, sticky=(tk.W, tk.E), pady=20)

        # Upload Images button
        self.norm_wavs = tk.Button(master=master, text="          Normalize images", bg="medium aquamarine",
                                    command=self.normalize_all_wavs, font="18",
                                    anchor=(tk.W)).grid(column=0, columnspan=2, row=3, sticky=(tk.W, tk.E), pady=20)


    def list_to_entry(self,evt):
        self.current_selection = self.mylist.curselection()
        self.current_value = self.mylist.get(self.mylist.curselection())
        self.mylist.bind("<Delete>", self.OnDeleteImage)
        self.mylist.bind("<Double-Button-1>", self.OnDouble)


    def rClicker(self, e):
        try:
            # Load .wav files
            def rClick_OpenWav(e, apnd=0):
                self.load_wav_image()

            # delete image
            def rClick_Delete(e):
                self.mylist.delete(self.current_selection)
                os.remove(os.getcwd() + "\Images\\" + self.current_value + ".wav")
                self.refresh()

            # translate to text
            def rClick_ToText(e):
                self.current_path = os.getcwd() + "\Images\\" + self.current_value + ".wav"
                self.speach_to_text = SpeachToText(self.model_for_recog, self.current_path)
                recog_file = self.speach_to_text.recognize_wav()
                tk.messagebox.showinfo(title="Text:", message=recog_file)

            #View .wav - form
            def rClick_OpenBio(e):
                self.load_bio_image()

            e.widget.focus()
            nclst = [
                (' Delete', lambda e=e: rClick_Delete(e)),
                (' Open .wav-form', lambda e=e: rClick_OpenWav(e)),
                (' Open biometric portrait', lambda e=e: rClick_OpenBio(e)),
                (' Convert to text', lambda e=e: rClick_ToText(e)),
            ]

            rmenu = tk.Menu(None, tearoff=0, takefocus=0)
            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)
            rmenu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

        except tk.TclError:
            print(' - rClick menu, something wrong')
            pass
        return "break"

    def rClickbinder(self, r):
        try:
            for b in ['Text', 'Entry', 'Listbox', 'Label']:  #
                r.bind_class(b, sequence='<Button-3>',
                             func=self.rClicker, add='')
        except tk.TclError:
            print(' - rClickbinder, something wrong')
            pass

    def buttonClickedDeleteAllImages(self):
        self.mylist.delete(0, self.mylist.size())
        filelist = [f for f in os.listdir("Images")]
        #print(filelist)
        for f in filelist:
            if f.endswith(".wav"):
                os.remove(os.path.join("Images", f))
        self.refresh()

    def buttonClickedAddImages(self):
        fileselect = tk.filedialog.askopenfilenames(parent=self, initialdir=os.getcwd() + "\Images",
                                                    title="Select .wav files to download",
                                                    filetypes=(("Audio Files", ".wav .ogg"), ("All Files", "*.*")))
        for file in fileselect:
            index_check = file.rfind("/")+1
            temp_file_check = file[:index_check-1]
            previous_folder_index = temp_file_check.rfind("/")+1
            previous_folder = temp_file_check[previous_folder_index:]
            if previous_folder == "Images":
                tk.messagebox.showerror("Mistake", "Image has already been added!")
            else:
                if file.endswith(".wav"):
                    index = file.rfind("/")+1
                    self.mylist.insert(tk.END, file[index:-4])
                shutil.copy2(file,os.getcwd() + "\Images")
        self.rename_all_after("Images")
        self.refresh()

    def OnOneClickListOfImage(self, event):
        selection = self.mylist.curselection()


    def OnDeleteImage(self, event):
        self.mylist.delete(self.current_selection)
        os.remove(os.getcwd() + "\Images\\" + self.current_value + ".wav")
        self.refresh()

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        self.load_wav_image()

    def load_wav_image(self):
        self.newWindow_wav_load = tk.Toplevel()
        self.newWindow_wav_load.title(self.current_value)
        self.newWindow_wav_load.minsize(width=1050, height=800)
        pygame.init()
        path = "Images/" + self.current_value + ".wav"
        spf = wave.open(path, "r")
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        spf.close()
        self.play = pygame.mixer.music
        self.play.load(path)
        fig = plt.Figure(facecolor='white')
        canvas = FigureCanvasTkAgg(fig, master=self.newWindow_wav_load)
        toolbar = NavigationToolbar(canvas, self.newWindow_wav_load)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        time_vect = np.arange(len(signal), dtype=np.float32) / 4000 * 1000
        ax_top = fig.add_subplot(111)
        ax_top.set_ylim(signal.min(), signal.max())
        ax_top.set_xlim(0, len(signal) / 4)
        ax_top.set_xlabel(u'time (ms)', fontsize=10)
        line_top, = ax_top.plot(time_vect, np.ones_like(time_vect))
        line_top.set_data(time_vect, signal)
        canvas.draw()
        self.button_play = tk.Button(master=self.newWindow_wav_load, bg="green2", font="85",
                                     image=play_image, compound=tk.LEFT, command=self.buttonPlayClicked)

        self.button_stop = tk.Button(master=self.newWindow_wav_load, bg="green2", font="85",
                                     image=stop_image, compound=tk.LEFT, command=self.buttonStopClicked)
        self.button_play.pack(side=tk.LEFT, expand=True)
        self.button_stop.pack(side=tk.RIGHT, expand=True)

        self.newWindow_wav_load.protocol('WM_DELETE_WINDOW', self.pygame_deactive)
        center(self.newWindow_wav_load)

    def pygame_deactive(self):
        pygame.mixer.quit()
        self.newWindow_wav_load.destroy()


    def load_bio_image(self):
        self.newWindow_bio_image = tk.Toplevel()
        self.newWindow_bio_image.title(self.current_value)
        self.newWindow_bio_image.minsize(width=1050,height=800)
        self.left_new_form = tk.Frame(master=self.newWindow_bio_image, bd=2, width=100, height=800, relief=tk.GROOVE)
        self.left_new_form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_new_form = tk.Frame(master=self.newWindow_bio_image, bd=2, width=50, height=800, relief=tk.SUNKEN)
        self.right_new_form.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.open_all_aliences()

        cur_path = [self.current_value + ".wav"]
        path = os.getcwd() + "/Images"
        bio_params = BioParams(path)

        df = create_df(cur_path)
        users_bio_params = df.apply(bio_params.extract_features, axis=1)

        self.current_bio_params = users_bio_params[0]
        self.signal = self.current_bio_params[0]
        self.fig = plt.Figure(facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_new_form)
        toolbar = NavigationToolbar(self.canvas, self.left_new_form)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.time_vect = np.arange(len(self.signal), dtype=np.float32)
        self.ax_top = self.fig.add_subplot(111)
        self.ax_top.set_ylim(self.signal.min(), self.signal.max())
        self.ax_top.set_xlim(0, len(self.signal) )
        self.ax_top.set_xlabel(u'number of parameters', fontsize=10)
        self.line_top, = self.ax_top.plot(self.time_vect, np.ones_like(self.time_vect))
        self.line_top.set_data(self.time_vect, self.signal)
        self.add_bio_radio_buttons(self.right_new_form)
        center(self.newWindow_bio_image)
        self.newWindow_bio_image.mainloop()

    def get_bio_koef(self):
        number = self.var.get()
        self.fig = plt.Figure(facecolor='white')
        self.signal = self.current_bio_params[number]
        self.time_vect = np.arange(len(self.signal), dtype=np.float32)
        self.ax_top.set_ylim(self.signal.min(), self.signal.max())
        self.ax_top.set_xlim(0, len(self.signal))
        self.line_top.set_data(self.time_vect, self.signal)
        self.canvas.draw()

    def calculate_all_svoi(self):
        path = os.getcwd() + "/Images"
        bio_params = BioParams(path)
        filelist_svoi = [f for f in os.listdir(path) if f.endswith('.wav')]
        df = create_df(filelist_svoi)
        users_bio_params = df.apply(bio_params.extract_features, axis=1)
        images = []
        size  = 0
        for par1 in range(len(users_bio_params)):
            for par2 in range(len(users_bio_params[par1])):
                for par3 in range(len(users_bio_params[par1][par2])):
                    images.append(float(users_bio_params[par1][par2][par3]))
            size += 1
        self.all_svoi = np.array(images)
        self.all_svoi.shape = (size, 194)


    def get_raspredelenie(self):
        self.newWindow_spreading = tk.Toplevel()
        self.newWindow_spreading.title(self.current_value)
        self.newWindow_spreading.minsize(width=1050, height=800)
        self.left_new_form_spreading = tk.Frame(master=self.newWindow_spreading, bd=2, width=100, height=800, relief=tk.GROOVE)
        self.left_new_form_spreading.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_new_form_spreading = tk.Frame(master=self.newWindow_spreading, bd=2, width=50, height=800, relief=tk.SUNKEN)
        self.right_new_form_spreading.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.calculate_all_svoi()

        svoi = []
        for par1 in range(len(self.current_bio_params)):
            for par2 in range(len(self.current_bio_params[par1])):
                svoi.append(float(self.current_bio_params[par1][par2]))

        distances_svoi_and_svoi = []
        svoinp = np.array(svoi)

        for sv in range(len(self.all_svoi)):
            dist = np.linalg.norm(svoinp - self.all_svoi[sv])
            if dist != 0:
                distances_svoi_and_svoi.append(dist)
        print(distances_svoi_and_svoi)
        snsplot = sns.distplot(distances_svoi_and_svoi, bins=len(self.all_svoi) - 1)
        self.fig_spreading = snsplot.get_figure()

        self.canvas_spreading = FigureCanvasTkAgg(self.fig_spreading, master=self.left_new_form_spreading)
        self.canvas_spreading.draw()
        self.canvas_spreading.get_tk_widget().pack()
        self.add_spreading_radio_buttons(self.right_new_form_spreading)
        center(self.newWindow_spreading)



    def add_bio_radio_buttons(self, selfmaster):
        self.var = tk.IntVar()

        tk.Radiobutton(master=selfmaster, text="Mel-frequency cepstral coefficients \n (MFCCs)",
                       command=self.get_bio_koef, variable=self.var, value=0).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Chromogram of the power spectrogram",
                       command=self.get_bio_koef, variable=self.var, value=1).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Spectrogram in chalk scale",
                       command=self.get_bio_koef, variable=self.var, value=2).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Spectral contrast",
                       command=self.get_bio_koef, variable=self.var, value=3).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="The tonal features of the centroid",
                       command=self.get_bio_koef, variable=self.var, value=4).pack(pady=20)

        tk.Button(master=selfmaster, text="Get the distribution of images",bg="green2", font="85",
                       command=self.get_raspredelenie).pack(pady=60)

        self.var.set(0)

    def open_all_aliences(self):
        file_all_aliens = open(os.getcwd() + '\\Alien\\all_aliences.txt', 'r')
        obraz = []
        size = 0
        for line in file_all_aliens:
            for x in line.split():
                obraz.append(float(x))
            size += 1
        self.all_aliens = np.array(obraz)
        self.all_aliens.shape = (size, 193)

        all_alliences_dist_file = open(os.getcwd() + "\\Alien\\\\all_alliences_dist.txt", "r")
        self.all_alliences_dist = []
        for line in all_alliences_dist_file:
            self.all_alliences_dist.append(line)

    def match_target_amplitude(self, sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)


    def normalize_all_wavs(self):
        filelist = [f for f in os.listdir("Images")]
        for f in filelist:
            if f.endswith(".wav"):
                sound = AudioSegment.from_file("Images\\" + f, "wav")
                normalized_sound = self.match_target_amplitude(sound, -20.0)
                normalized_sound.export("Images\\" + f, format="wav")


    def get_bio_spreading(self):
        number = self.var_spr.get()
        distances_svoi_and_svoi = []
        distances_svoi_aliences = []
        distances_svoi_relatively_all_svoi  = []
        distances_svoi_and_all_aliens = []

        svoi = []
        for par1 in range(len(self.current_bio_params)):
            for par2 in range(len(self.current_bio_params[par1])):
                svoi.append(float(self.current_bio_params[par1][par2]))
        svoinp = np.array(svoi)

        if number == 0:
            for sv in range(len(self.all_svoi)):
                dist = np.linalg.norm(svoinp - self.all_svoi[sv])
                if dist!=0:
                    distances_svoi_and_svoi.append(dist)
            print(distances_svoi_and_svoi)
            snsplot = sns.distplot(distances_svoi_and_svoi, bins=len(self.all_svoi)-1)
            self.fig_spreading = snsplot.get_figure()
            self.canvas_spreading.draw()

        if number ==1:
            current = 0
            for current in range(len(self.all_svoi)):
                for sv in range(len(self.all_svoi)):
                    if current != sv:
                        dist = np.linalg.norm(self.all_svoi[current] - self.all_svoi[sv])
                        distances_svoi_relatively_all_svoi.append(dist)
                current += 1
            snsplot = sns.distplot(distances_svoi_relatively_all_svoi, bins=len(self.all_svoi))
            self.fig_spreading = snsplot.get_figure()
            self.canvas_spreading.draw()

        if number == 2:
            current = 0
            for current in range(number + 1):
                for sv in range(len(self.all_aliens)):
                    if current != sv:
                        dist = np.linalg.norm(self.all_aliens[current] - self.all_aliens[sv])
                        distances_svoi_aliences.append(dist)
                current += 1
            snsplot = sns.distplot(distances_svoi_aliences, bins=30)
            self.fig_spreading = snsplot.get_figure()
            self.canvas_spreading.draw()

        if number == 3:
            for sv in range(len(self.all_aliens)):
                dist = np.linalg.norm(svoinp - self.all_aliens[sv])
                distances_svoi_and_all_aliens.append(dist)
            snsplot = sns.distplot(distances_svoi_and_all_aliens, bins=30)
            self.fig_spreading = snsplot.get_figure()
            self.canvas_spreading.draw()


    def add_spreading_radio_buttons(self, selfmaster):
        self.var_spr = tk.IntVar()

        tk.Radiobutton(master=selfmaster, text="The distribution of one image OWN\n relative to all of OWN",
                       command=self.get_bio_spreading, variable=self.var_spr, value=0).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Distribution of OWN relative to each other",
                       command=self.get_bio_spreading, variable=self.var_spr, value=1).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Distribution of ALL ALIENCES relative to each other",
                       command=self.get_bio_spreading, variable=self.var_spr, value=2).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Distribution of one OWN relative to all ALIENCES",
                       command=self.get_bio_spreading, variable=self.var_spr, value=3).pack(pady=20)

        self.var_spr.set(0)

    def buttonPlayClicked(self):
        self.play.play()

    def buttonStopClicked(self):
        self.play.stop()

    def add_wav_image_one(self, path, rowq, columnq, name):
        spf = wave.open(path, "r")
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        fig = plt.Figure(facecolor='white',figsize=(4, 3.5), dpi=80)
        canvas = FigureCanvasTkAgg(fig, master=self.newWindow)
        canvas.get_tk_widget().grid(row=rowq, column=columnq)

        time_vect = np.arange(len(signal), dtype=np.float32) / 4000 * 1000
        ax_top = fig.add_subplot(111)
        ax_top.set_ylim(signal.min(), signal.max())
        ax_top.set_xlim(0, len(signal) / 4)
        ax_top.set_xlabel(name, fontsize=6)
        line_top, = ax_top.plot(time_vect, np.ones_like(time_vect))
        line_top.set_data(time_vect, signal)
        canvas.draw()

    def rename_all(self, path, temp_variant):
        if temp_variant == 1:
            vart = "Images\empqweasdzxc №"
            filelist = [f for f in os.listdir(path)]
            if self.mylist.size()>1:
                filelist = sorted(filelist, key=lambda v: int(v.split('№')[-1][:-4]))
        else:
            vart = "Images\HuyPizdaDjigurda №"
            filelist = [f for f in os.listdir(path)]
            if self.mylist.size()>1:
                filelist = sorted(filelist, key=lambda v: int(v.split('№')[-1][:-4]))

        start = 1
        self.mylist.delete(0, self.mylist.size())
        for f in filelist:
            if f.endswith(".wav"):
                os.rename("Images\\" + f, vart + str(start) + ".wav")
                start += 1

    def rename_all_after(self, path):
        vart = "Images\HuyPizdaDjigurda №"
        filelist = [f for f in os.listdir(path)]
        print("1\n",filelist)
        start = 1
        self.mylist.delete(0, self.mylist.size())
        for f in filelist:
            if f.endswith(".wav"):
                os.rename("Images\\" + f, vart + str(start) + ".wav")
                start += 1

    def refresh(self):
        self.rename_all("Images",1)
        start = 1
        filelist_new = [f2 for f2 in os.listdir("Images")]
        filelist_new = sorted(filelist_new, key=lambda v: int(v.split('№')[-1][:-4]))
        for f2 in filelist_new:
            if f2.endswith(".wav"):
                os.rename("Images\\" + f2, "Images\Image №" + str(start) + ".wav")
                index = f2.rfind("/") + 1
                self.mylist.insert(tk.END, "Image №" + str(start))
                start += 1

    def save_rezults(self):
        file = os.path.join(os.getcwd(), "output.wav")
        new_file = os.path.join(os.getcwd(), "Image №999999.wav")
        shutil.copy2(file, os.getcwd() + "\Images")
        os.rename("Images\output.wav", "Images\Image №999999.wav")
        self.refresh()
        self.current_selection = self.mylist.size()
        self.mylist.select_set(self.current_selection-1)
        self.mylist.focus_set()