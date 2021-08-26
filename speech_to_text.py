from vosk import Model, KaldiRecognizer
import wave
import os
import time

class SpeachToText():
    def __init__(self,model,path):
        self.rec = 0
        self.final_rezult = ""
        self.model_for_recog = model
        self.current_path = path

    def recognize_wav(self):
        wf = wave.open(self.current_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            exit(1)

        rec = KaldiRecognizer(self.model_for_recog, wf.getframerate())
        rezult = ""
        rezerv_rezult = ""
        temp = ""
        self.final_rezult_temp = ""
        checkFin = 0
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                rec.Result()
                rezult = str(rec.Result())
                self.final_rezult += rezult[(rezult.find("text") + 9):-3]
                self.final_rezult += ". "
                self.final_rezult_temp = rezult[(rezult.find("text") + 9):-3] + ". "
                if rezult[(rezult.find("text") + 9):-3] != "":
                    checkFin = 1

            else:
                temp = str(rec.PartialResult())
                rezerv_rezult = temp[17:-3]
                checkFin = 0
                if self.final_rezult_temp == "":
                    rezerv_dlin_rezult = temp[17:-3]
                if self.final_rezult_temp == ". ":
                    self.final_rezult_temp = ""
                    self.final_rezult += rezerv_dlin_rezult + " "


        if checkFin == 0:
            self.final_rezult += rezerv_rezult
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace("  ", " ")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace(". ", "")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace(".", " ")
        old_recog_file = self.final_rezult

        old_recog_file = self.final_rezult
        if len(old_recog_file)>0:
            if old_recog_file[0] == " ":
                self.final_rezult =  old_recog_file[1:]
        if self.final_rezult == "" or self.final_rezult == "." or self.final_rezult == ". " or self.final_rezult == " ":
            self.final_rezult = rezerv_rezult

        # do not pay attention to it - it was necessary
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace(".", " ")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace("  ", " ")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace("  ", " ")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace("  ", " ")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace("  ", " ")
        old_recog_file = self.final_rezult
        self.final_rezult = old_recog_file.replace("  ", " ")
        old_recog_file = self.final_rezult
        if len(old_recog_file)>0:
            if old_recog_file[0] == " ":
                self.final_rezult =  old_recog_file[1:]
        return self.final_rezult