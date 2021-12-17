import librosa
import numpy as np
from sample_project import Inference
from sample_project import hparams

"""
Voicebox_Helper interfaces with your project's inference class with minimal modifications.
"""

class Voicebox_Helper:
    def __init__(self):
        # Define any information that needs to be stored in the object
        # If your software package has an inference class, it can be instantiated here.
        self.source_spec = None
        self.target_spec = None
        self.inference = Inference()

    def load_source(self, voicebox):
        # Inputs: a Voicebox object with file path in voicebox.fpath
        # Outputs: wav (at voicebox sample rate)

        # Load wav at the project's sample rate
        wav, _ = librosa.load(str(voicebox.fpath), hparams.sample_rate)

        # Get the spectrogram and draw it
        self.source_spec = self.inference.wav2spec(wav)
        voicebox.draw_spec(self.source_spec, "source")

        # Resample wav to voicebox sample rate and return control to UI
        resampled_wav = librosa.resample(wav, hparams.sample_rate, voicebox.sample_rate)
        return resampled_wav
        
    def load_target(self, voicebox):
        # Inputs: a Voicebox object with file path in voicebox.fpath
        # Outputs: wav (at voicebox sample rate)

        # Load wav at the project's sample rate
        wav, _ = librosa.load(str(voicebox.fpath), hparams.sample_rate)

        # Get the spectrogram and draw it
        self.target_spec = self.inference.wav2spec(wav)
        voicebox.draw_spec(self.target_spec, "target")

        # Resample wav to voicebox sample rate and return control to UI
        resampled_wav = librosa.resample(wav, hparams.sample_rate, voicebox.sample_rate)
        return resampled_wav
        
    def convert(self, voicebox):
        # Inputs: a Voicebox object
        # Outputs: wav (at voicebox sample rate)

        # Refuse to perform conversion if we don't have required data
        # It is safe to return None
        if self.source_spec is None or self.target_spec is None:
            return None

        # Disable UI buttons to prevent user interaction while running inference
        # Buttons automatically reenable when control is returned to voicebox
        voicebox.disable_all_buttons()

        # The sample project inference operates on wavs instead of specs.
        # We should edit the helper class to store the wavs, but here we will demonstrate
        # getting the wavs from the voicebox object. Resampling is performed in case
        # voicebox uses a different sample rate than our project.
        source_wav = librosa.resample(voicebox.source_wav, hparams.sample_rate, voicebox.sample_rate)
        target_wav = librosa.resample(voicebox.target_wav, hparams.sample_rate, voicebox.sample_rate)

        # Perform inference 
        wav, spec = self.inference.perform_inference(source_wav, target_wav)

        # Draw the converted spectrogram
        voicebox.draw_spec(spec, "converted")

        # Resample wav to voicebox sample rate and return control to UI
        resampled_wav = librosa.resample(wav, hparams.sample_rate, voicebox.sample_rate)
        return resampled_wav
