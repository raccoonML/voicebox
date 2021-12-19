import librosa
import numpy as np
from argparse import Namespace

hparams = Namespace(sample_rate = 24000,
                    n_fft = 2048,
                    hop_length = 300,
                    win_length = 1200)

"""
This is a minimal example that illustrates how Voicebox can connect to an existing project.

Required elements for the voice conversion UI are:
self.sample_rate
self.source_action
self.target_action
self.converted_action
"""

class Sample_Project:
    def __init__(self):
        # Property needed for voicebox
        self.sample_rate = hparams.sample_rate

        # Initialization for project
        self.source_wav = None
        self.target_wav = None

    """
    The following action methods are called by Voicebox on button press
    Source: [Load] --> source_action
    Target: [Load] --> target_action
    Converted: [Convert] --> converted_action
    """

    def source_action(self, wav):
        # Inputs: wav (from voicebox)
        # Outputs: spec (to voicebox)
        self.source_wav = wav
        return self.wav2spec(self.source_wav)

    def target_action(self, wav):
        # Inputs: wav (from voicebox)
        # Outputs: spec (to voicebox)
        self.target_wav = wav
        return self.wav2spec(self.target_wav)

    def converted_action(self):
        # Inputs: None
        # Outputs: wav, spec (to voicebox)
        
        wav, spec = self.convert_voice(self.source_wav, self.target_wav)
        return wav, spec

    """
    Class methods below this line are not directly called by Voicebox
    """

    def wav2spec(self, wav):
        spec = librosa.stft(y=wav, n_fft=hparams.n_fft, hop_length=hparams.hop_length, win_length=hparams.win_length)
        # shape = (channels, frames)
        spec = np.abs(spec) 
        spec = 20 * np.log10(np.maximum(1e-5, spec))
        # shape = (frames, channels)
        return spec.T

    def convert_voice(self, source_wav, target_wav):
        # Inputs: source_wav, target_wav
        # Outputs: wav, spec
        # spec shape = (frames, channels)

        # For this demo we will just average the 2 audios.
        # An inference function could also operate on spectrograms.
        min_len = min(source_wav.shape[0], target_wav.shape[0])
        wav = (source_wav[:min_len] + target_wav[:min_len]) / 2
        spec = self.wav2spec(wav)

        return wav, spec
