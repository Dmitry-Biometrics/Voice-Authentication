import tkinter as tk
import os
from Biometric_params import *
from center import center
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from RecordingFile import *
import shutil
from LiveMicWidget import *
from bio_params_view import *
from speech_to_text import *
import pymorphy2
from pydub import AudioSegment, effects
import time
import RightMainForm

class NetTrain:
    def __init__(self, model, train_list):
        global btn_record_image
        btn_record_image = tk.PhotoImage(file=os.getcwd() + "\\res\\record.png")
        global voice_params_image
        voice_params_image = tk.PhotoImage(file=os.getcwd() + "\\res\\bio_params.png")
        global voice_to_text_image
        voice_to_text_image = tk.PhotoImage(file=os.getcwd() +"\\res\\wav_txt.png")
        global key_image
        key_image = tk.PhotoImage(file=os.getcwd() + "\\res\\key_image.png")
        self.model_for_recog = model
        global btn_train_image
        btn_train_image = tk.PhotoImage(file=os.getcwd() +"\\res\\neuron.png")
        self.mylist = train_list

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
        f_mat = open(os.getcwd() + '\\Alien\\mat_og_all_aliences.txt', 'r')
        f_std = open(os.getcwd() + '\\Alien\\std_all_aliences.txt', 'r')
        self.mat_og_aliences = self.load_data(f_mat)
        self.std_aliences = self.load_data(f_std)

    def buttonClickedTrain(self):
        self.voice_to_text()
        self.newWindow = tk.Toplevel()
        self.newWindow.title("User Authentication")
        self.newWindow.focus_set()
        self.newWindow.minsize(width=1050, height=800)
        leftform = tk.Frame(master=self.newWindow, bd=2, width=800, height=80, relief=tk.GROOVE)
        leftform.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # authentication results
        rightform = tk.Frame(master=self.newWindow, bd=2, width=250, height=800, relief=tk.SUNKEN)
        rightform.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.button1_was_clicked = False
        self.recording_started = False
        self.recording_stopped = False
        self.get_container()
        self.Bioview = get_bio_params_view()
        self.porog, self.all_svoi, self.mat_og_svoi, self.std_svoi = self.Bioview.get_porog()


        LiveMicWidget(master=leftform)

        self.btn_start = tk.Button(master=leftform, text="Authentication", bg="green",font="85",
                                   image=btn_record_image,
                                   compound=tk.LEFT, command=self.buttonClickedRecord)

        self.btn_start.pack(side=tk.BOTTOM)

        self.btn_voice_txt = tk.Button(master=rightform, text="Voice password options",  font="85",
                                   image=voice_to_text_image ,bg="medium aquamarine",command=self.getListVoiceTxt,
                                   compound=tk.LEFT)
        self.btn_voice_txt.pack(pady = 80)


        self.btn_get_bio_params = tk.Button(master=rightform, text="Biometric \n parameters",
                                            image=voice_params_image, bg="medium aquamarine",
                                            command=self.Bioview.buttonClickedGetBio,
                                            font="18", compound=tk.LEFT)
        self.btn_get_bio_params.pack(pady=50)




        self.btn_additional_training  = tk.Button(master=rightform, text="Additional training ",
                                     image = btn_train_image,
                                     bg="medium aquamarine",
                                     command=self.additional_training,
                                     font="18", compound=tk.LEFT)
        self.btn_additional_training.pack(pady=40)

        self.newWindow.protocol('WM_DELETE_WINDOW', self.exit)
        self.save_container()
        center(self.newWindow)

    #Additional training, add an image to the container
    def additional_training(self):
        self.get_new_svoi()
        self.save_container()
        self.refresh_training_base()
        tk.messagebox.showinfo(title="Additional training ", message="Additional training completed ")

    def rename_all(self, path):
        vart = "Images\HuyPizdaDjigurda №"
        filelist = [f for f in os.listdir(path)]
        start = 1
        self.mylist.delete(0, self.mylist.size())
        for f in filelist:
            if f.endswith(".wav"):
                os.rename("Images \\" + f, vart + str(start) + ".wav")
                start += 1

    def refresh_training_base(self):
        self.rename_all("Images")
        start = 1
        filelist_new = [f2 for f2 in os.listdir("Images")]
        for f2 in filelist_new:
            if f2.endswith(".wav"):
                os.rename("Images\\" + f2, "Images\Image №" + str(start) + ".wav")
                index = f2.rfind("/") + 1
                self.mylist.insert(tk.END, "Image №" + str(start))
                start += 1

    #overwrite the "Own" parameters
    def get_new_svoi(self):
        users_bio_params = self.Bioview.get_bio_params(os.getcwd() + "\Testing\\")
        size = len(users_bio_params)
        images = []
        for zxc in range(len(users_bio_params)):
            len_bio_params = 0
            for qwe in range(len(users_bio_params[zxc])):
                signal = users_bio_params[zxc][qwe]
                for parametr in signal:
                    images.append(float(parametr))
                len_bio_params += len(signal)
        new_svoi_t = np.array(images)
        new_svoi_t.shape = (size, len_bio_params)
        self.new_svoi = self.norm(new_svoi_t)
        new_all_svoi = []
        for zxc in range(len(self.all_svoi)):
            for qwe in range(len(self.all_svoi[zxc])):
                new_all_svoi.append(self.all_svoi[zxc][qwe])
        for new_one in range(len(self.new_svoi)):
            new_all_svoi.append(self.new_svoi[new_one])
        new_svoi_t = np.array(new_all_svoi)
        new_svoi_t.shape = (len(self.all_svoi) + 1, len_bio_params-1)
        self.all_svoi = new_svoi_t
        self.mat_og_svoi = np.mean(self.all_svoi, axis=0)
        self.std_svoi = np.std(self.all_svoi, axis=0)

    #save bio-parameters container
    def save_container(self):
        fwrite = open('Testing\\svoi.txt', 'w')
        for zxc in range(len(self.all_svoi)):
            for asd in range(len(self.all_svoi[zxc])):
                fwrite.write(str(self.all_svoi[zxc][asd]) + "\t")
            fwrite.write("\n")

        fwrite2 = open('Testing\\mat_svoi.txt', 'w')
        for zxc in range(len(self.mat_og_svoi)):
            fwrite2.write(str(self.mat_og_svoi[zxc]) + "\t")

        fwrite3 = open('Testing\\std_svoi.txt', 'w')
        for zxc in range(len(self.std_svoi)):
            fwrite3.write(str(self.std_svoi[zxc]) + "\t")


    def exit(self):
        if os.path.exists(os.getcwd() + "\Images\\" + "Image_for_testing" + ".wav"):
            os.remove(os.getcwd() + "\Images\\" + "Image_for_testing" + ".wav")
        self.newWindow.destroy()

    #Normalize relative to the base "all ALLIENCES"
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

    #Calculate the distance between the test pattern and the expected value of the training sample
    def calculate_threshold(self):
        sample_for_test = os.getcwd() + "\Testing\Image_for_testing.wav"
        self.gottenparams = self.Bioview.get_bio_params(os.getcwd() + "\Testing")
        images = []
        size = len(self.gottenparams)
        images = []
        len_bio_params = 0
        for zxc in range(len(self.gottenparams)):
            len_bio_params = 0
            for qwe in range(len(self.gottenparams[zxc])):
                signal = self.gottenparams[zxc][qwe]
                for parametr in signal:
                    images.append(float(parametr))
                len_bio_params += len(signal)
        all_enemies_t = np.array(images)
        all_enemies_t.shape = (size, len_bio_params)
        self.all_enemies = self.norm(all_enemies_t)
        dist = 0
        self.until = 193


        for qwe in range(self.until):
            dist += ((self.all_enemies[qwe] - self.mat_og_svoi[qwe]) ** 2) / (self.std_svoi[qwe] ** 2)

        self.all_dist = math.sqrt(dist)
        print("difference  = ", self.all_dist)
        self.svoi_a = True
        if self.all_dist >= self.porog:
            print("ALLIEN")
            self.svoi_a = False
        if self.svoi_a:
            print("OWN")

    def match_target_amplitude(self, sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def buttonClickedRecord(self):
        was_start = False
        if self.btn_start["text"] == "Authentication" and not self.recording_started:
            print("writing an image for authentication")
            self.recording_file = RecordingFile(fname = os.getcwd() + "\Testing\\"+ "Image_for_testing.wav",
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
            print("finished recording ")
            sound = AudioSegment.from_file(os.getcwd() + "\Testing\\"+ "Image_for_testing.wav", "wav")
            normalized_sound = self.match_target_amplitude(sound, -20.0)
            normalized_sound.export(os.getcwd() + "\\Testing\\"+ "Image_for_testing.wav", format="wav")

            self.speach_to_text = SpeachToText(self.model_for_recog, os.getcwd() + "\\Testing\\"+ "Image_for_testing.wav")
            current_max_number = 0
            current_test_sbor = "Image_for_testing №1.wav"
            for f in os.listdir(os.getcwd() + "\\Testing\\Any collection"):
                if f.endswith('.wav'):
                    index = f.find("№") + 1
                    if current_max_number < int(f[index:-4]):
                        current_max_number = int(f[index:-4])
                        current_test_sbor = "Image_for_testing №" + str(current_max_number) + ".wav"
            shutil.copy2(os.getcwd() + "\Testing\Image_for_testing.wav", os.getcwd() + "\Testing\Any collection")
            os.rename(os.getcwd() + "\Testing\Any collection\Image_for_testing.wav", os.getcwd() + "\Testing\Any collection\\" + "Image_for_testing №" + str(current_max_number + 1) + ".wav")
            recog_file = self.speach_to_text.recognize_wav()
            old_recog_file = recog_file
            recog_file = old_recog_file.replace(".", "")
            parol = recog_file.split()
            current_recog = 0
            dlina_parol = len(parol)
            svoi = 0
            if len(parol)==0:
                svoi = 0
            else:
                for asd in range(len(self.all_lexeme_variants)):
                    if len(parol)!= len(self.all_lexeme_variants[asd]):
                        print("the length of what was said does not match the length of the hypothesis")
                        continue
                    current_recog = 0
                    current_porydok = 0

                    for zxc in range(len(self.all_lexeme_variants[asd])):
                        stroka = str(self.all_lexeme_variants[asd][zxc].keys())
                        if ("'" + parol[current_porydok] + "'") in stroka:
                            current_recog += 1
                            current_porydok += 1

                    kol_variants = len(self.all_lexeme_variants[asd])
                    if dlina_parol == current_recog and dlina_parol == kol_variants and dlina_parol!=0:
                        svoi = 1
                        break
                    current_recog = 0

            self.calculate_threshold()

            if svoi == 1 and self.svoi_a:
                tk.messagebox.showinfo(title="User Authentication", message = "Access is allowed\nPassword: \n" + recog_file
                    + "\nDistance:\n" + str(self.all_dist) + "\nMaximum threshold: " + str(self.porog))
            else:
                tk.messagebox.showerror(title="User Authentication", message = "Access is denied\nPassword: \n" + recog_file
                    + "\nDistance:\n" + str(self.all_dist) + "\nMaximum threshold: " + str(self.porog))
            self.newWindow.focus_set()
            shutil.copy2(os.getcwd() + "\Testing\\"+ "Image_for_testing.wav",os.getcwd() + "\Images")
            self.btn_start.config(text="Authentication")
            self.btn_start.config(bg="green")

            #Output to txt add-on
            file_dist = open(os.getcwd() + "\Testing\distances.txt", 'a')
            file_dist.write("Distance = " + str(self.all_dist) + "\n")


    #Convert speech to text
    def voice_to_text(self):
        path = os.getcwd() + "\Images"
        filelist = [f for f in os.listdir(path) if f.endswith('.wav')]
        self.original_recog = {}
        self.variants_recog = {}
        var = 0
        for file in filelist:
            file_to_recog = path + "\\"+ file
            self.speach_to_text = SpeachToText(self.model_for_recog, file_to_recog)
            recog_file = self.speach_to_text.recognize_wav()
            self.variants_recog[recog_file] = 0
            self.original_recog[file] = recog_file
            var += 1
        f_orig = open(os.getcwd() +  "\Testing\\rezult.txt", "w")
        f_variants = open(os.getcwd() +  "\Testing\\variants.txt", "w")
        for or_slovo in self.original_recog:
            if self.original_recog[or_slovo]!="":
                f_orig.write(str(or_slovo[:-4]) + " - " + str(self.original_recog[or_slovo]) + "\n")
            else:
                tk.messagebox.showinfo(title="Warning  ", message=or_slovo[:-4] + " - empty (Recording failed)")
        for or_slovo in self.variants_recog:
            f_variants.write(str(or_slovo) + "\n")
        self.lexeme_variants()


    #get all kinds of variations of each word
    def lexeme_variants(self):
        temp_dic = {}
        self.all_lexeme_variants = []
        one_of_variant = []
        morph = pymorphy2.MorphAnalyzer()
        for item in self.variants_recog:
            parol = item.split()
            one_of_variant = []
            for slovo in parol:
                slovo_par = morph.parse(slovo)[0]
                temp_dic = {}
                for i in range(len(slovo_par.lexeme)):
                    current_slovo = str(slovo_par.lexeme[i])
                    index = current_slovo.find("word") + 6
                    index2 = current_slovo.find("', tag")
                    word = current_slovo[index:index2]
                    temp_dic[word] = 0
                    i += 1
                one_of_variant.append(temp_dic)
            vsego_variants = 1
            for qwe in range(len(one_of_variant)):
                vsego_variants *= len(one_of_variant[qwe])
            self.all_lexeme_variants.append(one_of_variant)


    #Get a list of translated phrases
    def getListVoiceTxt(self):
        WindowWords = tk.Toplevel()
        WindowWords.title("Password options")
        WindowWords.focus_set()
        WindowWords.minsize(width=1150, height=800)
        leftform = tk.Frame(master=WindowWords, bd=2, width=800, height=800, relief=tk.GROOVE)
        leftform.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # authentication results
        rightform = tk.Frame(master=WindowWords, bd=2, width=250, height=800, relief=tk.SUNKEN)
        rightform.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        leftLabel = tk.Label(leftform, text="Recognized", font=('Helvetica', 16))
        leftLabel.pack()
        rightLabel = tk.Label(rightform, text="Possible options", font=('Helvetica', 16))
        rightLabel.pack()
        scrollbarXl = tk.Scrollbar(leftform, orient=tk.HORIZONTAL)
        scrollbarXl.pack(side="bottom", fill="x")
        scrollbarYl = tk.Scrollbar(leftform, orient=tk.VERTICAL)
        scrollbarYl.pack(side="right", fill="y")

        original_list_box = tk.Listbox(leftform, width=70, height=40, font=('Helvetica', 12),
                                       xscrollcommand=scrollbarXl.set, yscrollcommand=scrollbarYl.set)
        original_list_box.pack()

        for item in self.original_recog:
            original_list_box.insert(tk.END, item[:-4]  + " - " + str(self.original_recog[item]))

        scrollbarXl.config(command=original_list_box.xview)
        scrollbarYl.config(command=original_list_box.yview)
        ##---------------------------------------------------------------------------------

        scrollbarXr = tk.Scrollbar(rightform, orient=tk.HORIZONTAL)
        scrollbarXr.pack(side="bottom", fill="x")
        scrollbarYr = tk.Scrollbar(rightform, orient=tk.VERTICAL)
        scrollbarYr.pack(side="right", fill="y")

        variants_list_box = tk.Listbox(rightform, width=70, height=40, font=('Helvetica', 12),
                                       xscrollcommand=scrollbarXr.set, yscrollcommand=scrollbarYr.set)
        variants_list_box.pack()
        per = 0
        for asd in range(len(self.all_lexeme_variants)):
            for zxc in range(len(self.all_lexeme_variants[asd])):
                stroka = str(self.all_lexeme_variants[asd][zxc].keys())
                variants_list_box.insert(tk.END, stroka[10:])
            variants_list_box.insert(tk.END, "-" * 500)

        scrollbarXr.config(command=variants_list_box.xview)
        scrollbarYr.config(command=variants_list_box.yview)
        center(WindowWords)