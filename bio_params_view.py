import tkinter as tk
import os
from Biometric_params import *
from center import center
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


import seaborn as sns

class get_bio_params_view():
    def __init__(self):
        pass

    def buttonClickedGetBio(self):
        self.newWindow = tk.Toplevel()
        self.newWindow.title("Biometric parameters of images")
        self.newWindow.focus_set()
        self.newWindow.minsize(width=1600, height=800)

        # everything on the left side of the layout
        self.leftform_from_bio = tk.Frame(master=self.newWindow, bd=2, width=100, height=800, relief=tk.GROOVE)
        self.leftform_from_bio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # everything on the right side of the layout
        self.rightform_from_bio = tk.Frame(master=self.newWindow, bd=2, width=220, height=800, relief=tk.SUNKEN)
        self.rightform_from_bio.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        menubar2 = tk.Menu(self.newWindow)
        filemenu2 = tk.Menu(menubar2, tearoff=2)
        filemenu2.add_command(label="Close", command=self.newWindow.destroy)
        filemenu2.add_command(label="On one chart", command=self.OnOneGraphBio)
        menubar2.add_cascade(label="View", menu=filemenu2)
        self.newWindow.config(menu=menubar2)
        self.open_all_aliences()
        self.get_all_svoi(True)
        self.calculate_enemy_params()

        self.var1 = tk.IntVar()
        self.var1.set(0)
        self.add_bio_radio_buttons(self.rightform_from_bio, self.get_bio_koef_all, self.var1)

        center(self.newWindow)
        self.newWindow.mainloop()

    def load_data(self,file):
        output_l = []
        for line in file:
            for x in line.split():
                output_l.append(float(x))
        output = np.array(output_l)
        if len(output_l) / 194 > 1:
            output.shape = (int(len(output_l) / 194), 194)
        return output

    def get_container(self):
        os.getcwd()
        f_mat = open(os.getcwd() + "\\Alien\\mat_og_all_aliences.txt", 'r')
        f_std = open(os.getcwd() + "\\Alien\\std_all_aliences.txt", 'r')
        self.mat_og_aliences = self.load_data(f_mat)
        self.std_aliences = self.load_data(f_std)


    def norm(self, images):
        norm_im = []
        for qwe in range(len(images)):
            for asd in range(len(self.mat_og_aliences) - 1):
                normed = (images[qwe][asd] - self.mat_og_aliences[asd]) / self.std_aliences[asd]
                norm_im.append(normed)
        output = np.array(norm_im)
        if len(norm_im) / 193 > 1:
            output.shape = (int(len(norm_im) / 193), 193)
        return output


    def get_all_svoi(self, with_gui):
        self.get_container()
        filelist = [f for f in os.listdir("Images")]
        rowq = 0
        columnq = 0
        self.users_bio_params = self.get_bio_params(os.getcwd() + "\Images\\")
        size = len(self.users_bio_params)
        if with_gui:
            for f in filelist:
                if f.endswith(".wav"):
                    if columnq == 4:
                        columnq = 0
                        rowq += 1
                    signal = self.users_bio_params[0][0]
                    self.add_bio_image(os.getcwd() + "/Images", rowq, columnq, f, signal)
                    columnq += 1

        images = []
        for zxc in range(len(self.users_bio_params)):
            len_bio_params = 0
            for qwe in range(len(self.users_bio_params[zxc])):
                signal = self.users_bio_params[zxc][qwe]
                for parametr in signal:
                    images.append(float(parametr))
                len_bio_params += len(signal)
        all_svoi_t = np.array(images)
        all_svoi_t.shape = (size, len_bio_params)
        self.all_svoi = self.norm(all_svoi_t)

    #Window showing biometric parameters in one graph
    def OnOneGraphBio(self):
        self.newWindow_on_one = tk.Toplevel()
        self.newWindow_on_one.title("Biometric parameters of images ")
        menubar2 = tk.Menu(self.newWindow_on_one)
        filemenu2 = tk.Menu(menubar2, tearoff=2)
        filemenu2.add_command(label="Close", command=self.newWindow_on_one.destroy)
        filemenu2.add_command(label="On one chart", command=self.OnOneGraphBio)
        menubar2.add_cascade(label="View", menu=filemenu2)
        self.newWindow_on_one.config(menu=menubar2)
        self.newWindow_on_one.minsize(width=1050,height=800)
        self.leftform_from_bio_on = tk.Frame(self.newWindow_on_one, width=700, height=800, relief=tk.GROOVE)
        self.leftform_from_bio_on.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # everything on the right side of the layout
        self.rightform_from_bio_on = tk.Frame(self.newWindow_on_one, width=350, height=800, relief=tk.SUNKEN)
        self.rightform_from_bio_on.pack()#side=tk.RIGHT, fill=tk.BOTH, expand=True)

        filelist = [f for f in os.listdir("Images")]
        self.fig_bio_on_one = plt.Figure(facecolor='white', figsize=(4, 3.5), dpi=80)
        self.canvas_bio_on_one = FigureCanvasTkAgg(self.fig_bio_on_one, master=self.leftform_from_bio_on)
        self.canvas_bio_on_one.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas_bio_on_one.draw()
        number_f = 0
        for f in filelist:
            if f.endswith(".wav"):
                current_bio_params = self.users_bio_params[number_f]
                signal = current_bio_params[0]
                time_vect = np.arange(len(signal), dtype=np.float32)
                ax_top = self.fig_bio_on_one.add_subplot(111)
                ax_top.set_ylim(signal.min(), signal.max())
                ax_top.set_xlim(0, len(signal))
                line_top, = ax_top.plot(time_vect, np.ones_like(time_vect), label=f[:-4])
                ax_top.legend()
                line_top.set_data(time_vect, signal)
                self.canvas_bio_on_one.draw()
                number_f += 1
        self.var2 = tk.IntVar()
        self.var2.set(0)
        self.add_bio_radio_buttons(self.rightform_from_bio_on, self.get_bio_koef_on_one,self.var2)
        center(self.newWindow_on_one)
        self.newWindow_on_one.mainloop()

    #get an image of biomaterial parameters
    def add_bio_image(self, path, rowq, columnq, name, signal):
        fig = plt.Figure(facecolor='white',figsize=(4, 3.5), dpi=80)
        canvas = FigureCanvasTkAgg(fig, master=self.leftform_from_bio)
        canvas.get_tk_widget().grid(row=rowq, column=columnq)
        time_vect = np.arange(len(signal), dtype=np.float32)
        ax_top = fig.add_subplot(111)
        ax_top.set_ylim(signal.min(), signal.max())
        ax_top.set_xlim(0, len(signal))
        ax_top.set_xlabel(name, fontsize=6)
        line_top, = ax_top.plot(time_vect, np.ones_like(time_vect))
        line_top.set_data(time_vect, signal)
        canvas.draw()

    #threshold function
    def get_porog(self):
        self.get_all_svoi(False)
        self.mat_og_svoi = np.mean(self.all_svoi, axis=0)
        self.std_svoi = np.std(self.all_svoi, axis=0)
        current = 0
        self.until = 193
        distances_svoi_relatively_all_svoi = []
        for current in range(len(self.all_svoi)):
            dist = 0
            for qwe in range(self.until):
                dist += ((self.all_svoi[current][qwe] - self.mat_og_svoi[qwe]) ** 2) / (self.std_svoi[qwe] ** 2)
            distances_svoi_relatively_all_svoi.append(math.sqrt(dist))
            current += 1
        self.dist_svoi_relatively_all_svoi = np.array(distances_svoi_relatively_all_svoi)

        print("expected value = ", np.mean(self.dist_svoi_relatively_all_svoi))
        # Setting the threshold is situational, depending on the length of the phrase, the nature of the person himself, the environment at the time of authentication
        #porog = 2*np.mean(self.dist_svoi_relatively_all_svoi) #for short phrases and unstable people
        porog = np.mean(self.dist_svoi_relatively_all_svoi) + (3 * np.std(self.dist_svoi_relatively_all_svoi))  #для длинных фраз (from 15 сек)
        # porog = max(self.dist_svoi_relatively_all_svoi) # for stable people who have completed additional training
        print("maximum threshold  = ", porog)
        return porog, self.all_svoi, self.mat_og_svoi, self.std_svoi


    def get_all_signals_distributions(self):
        one_svoi = []
        distances_svoi_and_svoi = []
        for number in range(len(self.all_svoi)):
            for par1 in range(len(self.all_svoi[number])):
                one_svoi.append(self.all_svoi[number][par1])
            svoinp = np.array(one_svoi)
            for sv in range(len(self.all_svoi)):
                dist = np.linalg.norm(svoinp - self.all_svoi[sv])
                if number != sv:
                    distances_svoi_and_svoi.append(dist)
            one_svoi = []
        self.dist_svoi_and_svoi = np.array(distances_svoi_and_svoi)
        self.dist_svoi_and_svoi.shape = (len(self.all_svoi),len(self.all_svoi)-1)

        one_svoi = []
        distances_svoi_and_all_aliences = []
        for number in range(len(self.all_svoi)):
            for par1 in range(len(self.all_svoi[number])):
                one_svoi.append(self.all_svoi[number][par1])
            svoinpa = np.array(one_svoi)
            for sv in range(len(self.all_aliens)):
                dist = np.linalg.norm(svoinpa - self.all_aliens[sv])
                if number != sv:
                    distances_svoi_and_all_aliences.append(dist)
            one_svoi = []

        self.dist_svoi_and_all_aliences = np.array(distances_svoi_and_all_aliences)
        self.dist_svoi_and_all_aliences.shape = (len(self.all_svoi), len(self.all_aliens) - 1)

        current = 0
        distances_svoi_relatively_all_svoi = []
        for current in range(len(self.all_svoi)):
            for sv in range(len(self.all_svoi)):
                if current != sv:
                    dist = np.linalg.norm(self.all_svoi[current] - self.all_svoi[sv])
                    distances_svoi_relatively_all_svoi.append(dist)
            current += 1
        self.dist_svoi_relatively_all_svoi = np.array(distances_svoi_relatively_all_svoi)

        current = 0
        distances_allaliences = []
        number_of_alliences = 3
        for current in range(number_of_alliences):
            for sv in range(len(self.all_aliens)):
                if current != sv:
                    dist = np.linalg.norm(self.all_aliens[current] - self.all_aliens[sv])
                    distances_allaliences.append(dist)
            current += 1
        self.dist_allaliences = np.array(distances_allaliences)

        current = 0
        distance_svoi_enemy = []
        for current in range(len(self.all_svoi)):
            for sv in range(len(self.all_enemies)):
                    dist = np.linalg.norm(self.all_svoi[current] - self.all_enemies[sv])
                    distance_svoi_enemy.append(dist)
            current += 1
        self.dist_svoi_enemy = np.array(distance_svoi_enemy)
        # I can't fit more than 16 on my monitor, and I was too lazy to do scrolling
        self.until = 16
        if len(self.dist_svoi_and_svoi) < 16:
            self.until = len(self.dist_svoi_and_svoi)


    def add_raspredelenie_image(self):
        self.f_spread = Figure(figsize=(10, 10))
        self.axes = self.f_spread.subplots(4, 4, sharex=False, sharey=False)
        self.canvas_spreading = FigureCanvasTkAgg(self.f_spread, master=self.left_new_form_spreading)
        self.canvas_spreading.get_tk_widget().pack()
        variants_of_color = ["skyblue", "olive", "gold", "teal", "red", "green", "blue", "purple", "orange", "green", "pink", "silver", "skyblue", "olive", "gold", "teal", "red", "green", "blue", "purple", "orange", "green", "pink", "silver"]
        until = 16
        if len(self.dist_svoi_and_svoi)<16:
            until = len(self.dist_svoi_and_svoi)

        row = 0
        column = 0
        for num in range(until):
            sns.distplot(self.dist_svoi_and_svoi[num], color=variants_of_color[num], ax=self.axes[row, column], bins=10)
            column +=1
            if column == 4:
                row +=1
                column = 0
        self.canvas_spreading.draw()


    def add_bio_radio_buttons(self, selfmaster, commanda, variant):

        tk.Radiobutton(master=selfmaster, text="Mel-frequency cepstral coefficients \n (MFCCs)",
                       command=commanda, variable=variant, value=0).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Chromogram of the power spectrogram",
                       command=commanda, variable=variant, value=1).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Spectrogram in chalk scale",
                       command=commanda, variable=variant, value=2).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="Spectral contrast",
                       command=commanda, variable=variant, value=3).pack(pady=20)

        tk.Radiobutton(master=selfmaster, text="The tonal features of the centroid",
                       command=commanda, variable=variant, value=4).pack(pady=20)

        tk.Button(master=selfmaster, text="Get the distribution of images", bg="green2",
                  command=self.get_raspredelenie
                  ).pack(pady=20)

    def get_raspredelenie(self):
        self.newWindow_spreading = tk.Toplevel()
        self.newWindow_spreading.title("Image distributions")
        self.newWindow_spreading.minsize(width=1050, height=800)
        self.left_new_form_spreading = tk.Frame(master=self.newWindow_spreading, bd=2, width=100, height=800, relief=tk.GROOVE)
        self.left_new_form_spreading.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_new_form_spreading = tk.Frame(master=self.newWindow_spreading, bd=2, width=50, height=800, relief=tk.SUNKEN)
        self.right_new_form_spreading.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        self.get_all_signals_distributions()
        self.add_raspredelenie_image()
        self.add_spreading_check_buttons(self.right_new_form_spreading)
        tk.Label(master=self.right_new_form_spreading, text="One's OWN relative to all one's OWN :\n from " + str(np.format_float_positional(np.float16(np.min(self.dist_svoi_and_svoi))))
          + "  to  "   + str(np.format_float_positional(np.float16(np.max(self.dist_svoi_and_svoi))))).pack(pady=20)
        tk.Label(master=self.right_new_form_spreading, text="OWN relative to each other:\n from " + str(np.format_float_positional(np.float16(np.min(self.dist_svoi_relatively_all_svoi))))
          + "  to  "   + str(np.format_float_positional(np.float16(np.max(self.dist_svoi_relatively_all_svoi))))).pack(pady=20)
        tk.Label(master=self.right_new_form_spreading, text="All ENEMEIES relative to each other :\n from " + str(np.format_float_positional(np.float16(np.min(self.dist_svoi_and_all_aliences))))
          + "  to  "   + str(np.format_float_positional(np.float16(np.max(self.dist_svoi_and_all_aliences))))).pack(pady=20)
        tk.Label(master=self.right_new_form_spreading, text="OWN relative to all ENEMEIES :\n from " + str(np.format_float_positional(np.float16(np.min(self.dist_allaliences))))
          + "  to  "   + str(np.format_float_positional(np.float16(np.max(self.dist_allaliences))))).pack(pady=20)
        tk.Label(master=self.right_new_form_spreading, text="An attacker in relation to all OWN :\n from " + str(np.format_float_positional(np.float16(np.min(self.dist_svoi_enemy))))
          + "  to  "   + str(np.format_float_positional(np.float16(np.max(self.dist_svoi_enemy))))).pack(pady=20)

        center(self.newWindow_spreading)

    def add_spreading_check_buttons(self, selfmaster):
        self.var_spr = tk.BooleanVar()
        self.ax_already_exist = 0

        tk.Checkbutton(master=selfmaster, text="The distribution of one image OWN\n relative to all of OWN",
                        command = self.get_first_spreading , variable=self.var_spr).pack(pady=20)
        self.var_spr.set(True)


        self.var_spr2 = tk.BooleanVar()
        self.var_spr2.set(False)
        tk.Checkbutton(master=selfmaster, text="Distribution of OWN relative to each other",
                       command=self.get_second_spreading, variable=self.var_spr2).pack(pady=20)

        self.var_spr3 = tk.BooleanVar()
        self.var_spr3.set(False)
        tk.Checkbutton(master=selfmaster, text="Distribution of ALL ALIENCES relative to each other",
                       command=self.get_third_spreading, variable=self.var_spr3).pack(pady=20)

        self.var_spr4 = tk.BooleanVar()
        self.var_spr4.set(False)
        tk.Checkbutton(master=selfmaster, text="Distribution of one OWN relative to all ALIENCES",
                       command=self.get_fourth_spreading, variable=self.var_spr4).pack(pady=20)


        self.var_spr5 = tk.BooleanVar()
        self.var_spr5.set(False)
        tk.Checkbutton(master=selfmaster, text="The distribution of the cracker relative to all OWN",
                       command=self.get_fifth_spreading, variable=self.var_spr5).pack(pady=20)


    def delete_first(self):
        self.f_spread.clear()
        plt.clf()
        self.canvas_spreading.draw()

    def get_first_spreading(self):
        if self.var_spr.get() == True:
            if self.var_spr2.get() == True or self.var_spr3.get() == True or self.var_spr5.get() == True:
                self.delete_first()
                self.var_spr2.set(False)
                self.var_spr3.set(False)
                self.var_spr5.set(False)
            if self.var_spr4.get() == False:
                self.axes = self.f_spread.subplots(4, 4, sharex=False, sharey=False)
            variants_of_color = ["skyblue", "olive", "gold", "teal", "red", "green", "blue", "purple", "orange",
                                 "green", "pink", "silver","skyblue", "olive", "gold", "teal", "red", "green", "blue", "purple", "orange",
                                 "green", "pink", "silver"]
            row = 0
            column = 0
            for num in range(self.until):
                sns.distplot(self.dist_svoi_and_svoi[num], color=variants_of_color[num], ax=self.axes[row, column], bins=10)
                column += 1
                if column == 4:
                    row += 1
                    column = 0
            self.canvas_spreading.draw()
            self.var_spr4.set(False)

        if self.var_spr.get() == False:
            self.delete_first()

    def get_second_spreading(self):
        if self.var_spr2.get() == True:
            if self.var_spr.get() == True:
                self.delete_first()
                self.var_spr.set(False)
                self.var_spr4.set(False)
            if self.ax_already_exist == 0:
                self.axes = self.f_spread.subplots(sharex=False, sharey=False)
            sns.distplot(self.dist_svoi_relatively_all_svoi, color="green",  bins=10, ax = self.axes)
            self.ax_already_exist = 1
            self.canvas_spreading.draw()

        if self.var_spr2.get() == False:
            self.delete_first()
            self.var_spr3.set(False)
            self.var_spr5.set(False)
            self.ax_already_exist = 0

    def get_third_spreading(self):
        if self.var_spr3.get() == True:
            if self.var_spr.get() == True or self.var_spr4.get() == True:
                self.delete_first()
                self.var_spr.set(False)
                self.var_spr4.set(False)

            print(self.axes)
            if self.ax_already_exist == 0:
                self.axes = self.f_spread.subplots(sharex=False, sharey=False)
            sns.distplot(self.dist_allaliences, color="red",  bins=10, ax = self.axes)
            self.ax_already_exist = 1
            self.canvas_spreading.draw()

        if self.var_spr3.get() == False:
            self.delete_first()
            self.var_spr2.set(False)
            self.ax_already_exist = 0

    def get_fourth_spreading(self):
        if self.var_spr4.get() == True:
            if self.var_spr2.get() == True or self.var_spr3.get() == True:
                self.delete_first()
                self.var_spr2.set(False)
                self.var_spr3.set(False)
                self.axes = self.f_spread.subplots(4, 4, sharex=False, sharey=False)

            if self.var_spr.get() == False:
                self.axes = self.f_spread.subplots(4, 4, sharex=False, sharey=False)
            variants_of_color = ["olive", "gold", "teal", "red", "green", "blue", "purple", "orange",
                                 "green", "pink", "silver","skyblue","olive", "gold", "teal", "red", "green", "blue", "purple", "orange",
                                 "green", "pink", "silver","skyblue"]

            row = 0
            column = 0
            for num in range(self.until):
                sns.distplot(self.dist_svoi_and_all_aliences[num],
                             color=variants_of_color[num],
                             ax=self.axes[row, column],
                             bins=10)
                column += 1
                if column == 4:
                    row += 1
                    column = 0
            self.canvas_spreading.draw()

        if self.var_spr4.get() == False:
            self.delete_first()
            self.var_spr.set(False)

    def get_fifth_spreading(self):
        if self.var_spr5.get() == True:
            if self.var_spr.get() == True or self.var_spr4.get() == True:
                self.delete_first()
                self.var_spr.set(False)
                self.var_spr4.set(False)

            if self.ax_already_exist == 0:
                self.axes = self.f_spread.subplots(sharex=False, sharey=False)
            self.ax_already_exist = 1
            sns.distplot(self.dist_svoi_enemy, color="blue", bins=10, ax=self.axes)
            self.canvas_spreading.draw()

        if self.var_spr5.get() == False:
            self.delete_first()
            self.var_spr2.set(False)
            self.var_spr3.set(False)
            self.ax_already_exist = 0

    def open_all_aliences(self):
        file_all_aliens = open('Alien\\all_aliences.txt', 'r')
        obraz = []
        size = 0
        for line in file_all_aliens:
            for x in line.split():
                obraz.append(float(x))
            size += 1
        self.all_aliens = np.array(obraz)
        self.all_aliens.shape = (size, 193)

        all_alliences_dist_file = open(os.getcwd() + "\Alien\\all_alliences_dist.txt", "r")
        self.all_alliences_dist = []
        size = 0
        for line in all_alliences_dist_file:
            self.all_alliences_dist.append(line)

    def get_bio_koef_all(self):
        number = self.var1.get()
        filelist = [f for f in os.listdir("Images")]
        rowq = 0
        columnq = 0
        number_f = 0
        for f in filelist:
            if f.endswith(".wav"):
                if columnq == 4:
                    columnq = 0
                    rowq += 1
                path = os.getcwd() + "/Images"
                current_bio_params = self.users_bio_params[number_f]
                signal = current_bio_params[number]
                self.add_bio_image(path, rowq, columnq, f, signal)
                columnq += 1
                number_f += 1

    def get_bio_raspredelenie_all(self):
        number = self.var1.get()
        filelist = [f for f in os.listdir("Images")]
        rowq = 0
        columnq = 0
        number_f = 0
        for f in filelist:
            if f.endswith(".wav"):
                if columnq == 4:
                    columnq = 0
                    rowq += 1
                path = os.getcwd() + "/Images"
                current_bio_params = self.users_bio_params[number_f]
                signal = current_bio_params[number]
                self.add_bio_image(path, rowq, columnq, f, signal)
                columnq += 1
                number_f += 1

    def get_bio_koef_on_one(self):
        number = self.var2.get()
        filelist = [f for f in os.listdir("Images")]
        self.fig_bio_on_one.clear()
        min_y = 100
        max_y = 0
        number_f = 0
        for f in filelist:
            if f.endswith(".wav"):
                current_bio_params = self.users_bio_params[number_f]
                signal = current_bio_params[number]
                if min(signal)<min_y:
                    min_y = min(signal)
                if  max(signal)> max_y:
                    max_y = max(signal)
                number_f += 1
        number_f = 0
        for f in filelist:
            if f.endswith(".wav"):
                current_bio_params = self.users_bio_params[number_f]
                signal = current_bio_params[number]
                time_vect = np.arange(len(signal), dtype=np.float32)
                ax_top = self.fig_bio_on_one.add_subplot(111)
                ax_top.set_ylim(min_y, max_y)
                ax_top.set_xlim(0, len(signal))
                line_top, = ax_top.plot(time_vect, np.ones_like(time_vect),label=f[:-4])
                ax_top.legend()
                line_top.set_data(time_vect, signal)
                self.canvas_bio_on_one.draw()
                number_f += 1

    def get_bio_params(self, path):
        bio_params = BioParams(path)
        filelist = [f for f in os.listdir(path) if f.endswith('.wav')]
        df = create_df(filelist)
        users_bio_params = df.apply(bio_params.extract_features, axis=1)
        return users_bio_params

    #for slickness, you can take images of a stranger to see the difference
    def calculate_enemy_params(self):
        rowq = 0
        columnq = 0
        self.enemy_bio_params = self.get_bio_params(os.getcwd() + "\enemy\\")
        size = len(self.enemy_bio_params)
        images = []
        len_bio_params = 0
        for zxc in range(len(self.enemy_bio_params)):
            len_bio_params = 0
            for qwe in range(len(self.enemy_bio_params [zxc])):
                signal = self.enemy_bio_params[zxc][qwe]
                for parametr in signal:
                    images.append(float(parametr))
                len_bio_params += len(signal)
        self.all_enemies_t = np.array(images)
        self.all_enemies_t.shape = (size, len_bio_params)
        self.all_enemies = self.norm(self.all_enemies_t)