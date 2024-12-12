import librosa
import numpy as np

from pulse.music_visualizer_video_maker.options import Options

class Visualizer:
    def __init__(self, audioFile):

        self.TimeSeries, self.SampleRate = librosa.load(audioFile, sr=Options.SAMPLE_RATE)

        self.Stft = np.abs(librosa.stft(self.TimeSeries, hop_length=Options.HOP_LENGTH, n_fft=Options.N_FFT))

        self.Spectrogram = librosa.amplitude_to_db(self.Stft, ref=np.max)

        self.Loudness = librosa.feature.rms(S=librosa.magphase(self.Stft)[0], hop_length=Options.HOP_LENGTH, frame_length=Options.N_FFT).flatten()
        

        self.OnsetEnvelope = librosa.onset.onset_strength(y=self.TimeSeries, sr=Options.SAMPLE_RATE, hop_length=Options.HOP_LENGTH)
        self.OnsetEnvelopeMin = np.amin(self.OnsetEnvelope)
        self.OnsetEnvelopeMax = np.amax(self.OnsetEnvelope)
        self.OnsetFrames = librosa.util.peak_pick(x=self.OnsetEnvelope, pre_max=7, post_max=7, pre_avg=7, post_avg=7, delta=0.5, wait=5)

        self.Frequencies = librosa.core.fft_frequencies(n_fft=Options.N_FFT)
        self.Times = librosa.core.frames_to_time(np.arange(self.Spectrogram.shape[1]), sr=Options.SAMPLE_RATE, hop_length=Options.HOP_LENGTH, n_fft=Options.N_FFT)
        self.TimeIndexRatio = len(self.Times) / self.Times[len(self.Times) - 1]
        self.FrequenciesIndexRatio = len(self.Frequencies) / self.Frequencies[len(self.Frequencies) - 1]

    
    def CreateLoudnessConvolved(self, kernelSize):
        kernel = np.ones(kernelSize) / kernelSize
        return np.convolve(self.Loudness, kernel)

    def GetFreqDb(self, time, freq):
        return self.Spectrogram[int(freq * self.FrequenciesIndexRatio)][int(time * self.TimeIndexRatio)]

    def GetMoment(self, time):
        return int(time * self.TimeIndexRatio)

    @staticmethod
    def Translate(value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    

    