import os
#import pandas as pd
import sys
import pandas as pd
import librosa
import numpy as np



def create_df(filelist):
    df = pd.DataFrame(filelist)
    df['user'] = '1'
    df = df.rename(columns={0: 'file'})
    return df


class BioParams:
    def __init__(self, path):                  # Инициализатор
        self.path_to = path

    def extract_features(self, files):
        # Sets the name to be the path to where the file is in my computer
        file_name = os.path.join(os.path.abspath(self.path_to) + '/' + str(files.file))

        # Loads the audio file as a floating point time series and assigns the default sample rate
        # Sample rate is set to 22050 by default
        X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')

        # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)

        # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
        stft = np.abs(librosa.stft(X))

        # Computes a chromagram from a waveform or power spectrogram.
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)

        # Computes a mel-scaled spectrogram.
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)

        # Computes spectral contrast
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)

        # Computes the tonal centroid features (tonnetz)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),sr=sample_rate).T, axis=0)

        # We add also the classes of each file as a label at the end
        label = files.user

        return mfccs, chroma, mel, contrast, tonnetz, label




