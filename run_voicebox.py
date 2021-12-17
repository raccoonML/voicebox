from voicebox import Voicebox
from voicebox_helper import Voicebox_Helper
from sample_project import hparams

if __name__ == '__main__':
    # Instantiate the helper, which in turn instantiates the project's inference class.
    helper = Voicebox_Helper()

    # Start voicebox
    Voicebox(helper.load_source, helper.load_target, helper.convert, hparams.sample_rate)
