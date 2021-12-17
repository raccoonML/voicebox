import librosa
import numpy as np
from argparse import Namespace

hparams = Namespace(sample_rate = 24000,
                    n_fft = 2048,
                    hop_length = 300,
                    win_length = 1200)

"""
This is a minimal example that illustrates how voicebox can connect to an existing project.
"""

class Inference:
    def __init__(self):
        return

    def wav2spec(self, wav):
        spec = librosa.stft(y=wav, n_fft=hparams.n_fft, hop_length=hparams.hop_length, win_length=hparams.win_length)
        # shape = (channels, frames)
        spec = np.abs(spec) 
        spec = 20 * np.log10(np.maximum(1e-5, spec))
        # shape = (frames, channels)
        return spec.T

    def perform_inference(self, source_wav, target_wav):
        # Inputs: source_wav, target_wav
        # Outputs: wav, spec
        # spec shape = (frames, channels)

        # For this demo we will just average the 2 audios.
        # An inference function could also operate on spectrograms.
        min_len = min(source_wav.shape[0], target_wav.shape[0])
        wav = (source_wav[:min_len] + target_wav[:min_len]) / 2
        spec = self.wav2spec(wav)

        return wav, spec
