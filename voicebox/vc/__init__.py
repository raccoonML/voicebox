from voicebox.vc.ui import UI
import librosa
import sys
import traceback

"""
Voicebox Voice Conversion

Your project needs to provide the following interfaces to use this Voicebox UI.

voice_obj.sample_rate          # Sample rate in Hz
voice_obj.source_action(wav)   # Class method to handle a loaded source wav, returns: spec
voice_obj.target_action(wav)   # Class method to handle a loaded target wav, returns: spec
voice_obj.converted_action()   # Class method to perform voice conversion, returns: wav, spec
"""

class Voicebox:
    def __init__(self, voice_obj, window_title=""):
        # Prevent errors from crashing the window
        sys.excepthook = self.excepthook

        # Process inputs
        self.voice_obj = voice_obj

        if len(window_title) == 0:
            window_title = "Voicebox"

        # Initialize variables
        self.source_wav = None
        self.target_wav = None
        self.converted_wav = None
        self.fpath = None

        # Initialize the events and the interface
        self.ui = UI(window_title)
        self.setup_events()
        self.update_buttons()
        self.ui.start()

    def excepthook(self, exc_type, exc_value, exc_tb):
        traceback.print_exception(exc_type, exc_value, exc_tb)
        self.ui.log("Exception: %s" % exc_value)
        
    def setup_events(self):
        ## Source
        # Load
        func = lambda: self.load_from_browser(self.ui.browse_file(), "source")
        self.ui.source_load_button.clicked.connect(func)
        # Play
        func = lambda: self.play("source") 
        self.ui.source_play_button.clicked.connect(func)

        ## Target
        # Load
        func = lambda: self.load_from_browser(self.ui.browse_file(), "target")
        self.ui.target_load_button.clicked.connect(func)
        # Play
        func = lambda: self.play("target") 
        self.ui.target_play_button.clicked.connect(func)

        ## Converted
        # Convert
        func = lambda: self.convert()
        self.ui.converted_conv_button.clicked.connect(func)
        # Play
        func = lambda: self.play("converted") 
        self.ui.converted_play_button.clicked.connect(func)
        # Save As
        func = lambda: self.save("converted")
        self.ui.converted_save_button.clicked.connect(func)

    def get_wav(self, wavtype):
        if wavtype == "source":
            return self.source_wav
        elif wavtype == "target":
            return self.target_wav
        else:
            return self.converted_wav

    def play(self, wavtype):
        self.ui.play(self.get_wav(wavtype), self.voice_obj.sample_rate)
        
    def save(self, wavtype):
        self.ui.save_audio_file(self.get_wav(wavtype), self.voice_obj.sample_rate)

    def load_from_browser(self, fpath, wavtype):
        if fpath == "":
            return 

        # Load wav at the project's sample rate
        wav, _ = librosa.load(str(fpath), self.voice_obj.sample_rate)

        # Provide voice object with the wav
        if wavtype == "source":
            self.source_wav = wav
            spec = self.voice_obj.source_action(wav)
        else:
            self.target_wav = wav
            spec = self.voice_obj.target_action(wav)

        # Draw the spectrogram
        if spec is not None:
            self.draw_spec(spec, wavtype)

        self.update_buttons()

    def convert(self):
        # Call the conversion
        self.converted_wav, spec = self.voice_obj.converted_action()
        # Draw the spectrogram
        if spec is not None:
            self.draw_spec(spec, "converted")

        self.update_buttons()

    def draw_spec(self, spec, wavtype):
        # Draw spec
        self.ui.draw_spec(spec, wavtype)

    def update_buttons(self):
        # Always allow loading of source/target
        self.ui.source_load_button.setDisabled(False)
        self.ui.target_load_button.setDisabled(False)

        # Enable play/save buttons if wav exists
        if self.source_wav is None:
            self.ui.source_play_button.setDisabled(True)
        else:
            self.ui.source_play_button.setDisabled(False)
            
        if self.target_wav is None:
            self.ui.target_play_button.setDisabled(True)
        else:
            self.ui.target_play_button.setDisabled(False)

        if self.converted_wav is None:
            self.ui.converted_play_button.setDisabled(True)
            self.ui.converted_save_button.setDisabled(True)
        else:
            self.ui.converted_play_button.setDisabled(False)
            self.ui.converted_save_button.setDisabled(False)

        # Enable convert button when both source and target exist
        if self.source_wav is None or self.target_wav is None:
            self.ui.converted_conv_button.setDisabled(True)
        else:
            self.ui.converted_conv_button.setDisabled(False)
