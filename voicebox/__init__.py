from voicebox.ui import UI
import traceback
import sys

class Voicebox:
    def __init__(self, source_func, target_func, converted_func, sample_rate, window_title=""):
        # Prevent errors from crashing the window
        sys.excepthook = self.excepthook

        # Initialize variables
        self.source_func = source_func
        self.target_func = target_func
        self.converted_func = converted_func
        self.sample_rate = sample_rate

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
        self.ui.play(self.get_wav(wavtype), self.sample_rate)
        
    def save(self, wavtype):
        self.ui.save_audio_file(self.get_wav(wavtype), self.sample_rate)

    def load_from_browser(self, fpath, wavtype):
        if fpath == "":
            return 
        else:
            self.fpath = fpath

        if wavtype == "source":
            self.source_wav = self.source_func(self)
        if wavtype == "target":
            self.target_wav = self.target_func(self)
        self.update_buttons()

    def convert(self):
        self.converted_wav = self.converted_func(self)
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

    def disable_all_buttons(self):
            self.ui.source_load_button.setDisabled(True)
            self.ui.source_play_button.setDisabled(True)
            self.ui.target_load_button.setDisabled(True)
            self.ui.target_play_button.setDisabled(True)
            self.ui.converted_conv_button.setDisabled(True)
            self.ui.converted_play_button.setDisabled(True)
            self.ui.converted_save_button.setDisabled(True)
