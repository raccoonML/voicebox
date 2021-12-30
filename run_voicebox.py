import argparse
from examples.vc.sample_vc_project import Sample_Project as Sample_VC_Project
from examples.vocoder.sample_vocoder_project import Sample_Project as Sample_Vocoder_Project
from voicebox.vc import Voicebox as Voicebox_VC
from voicebox.vocoder import Voicebox as Voicebox_Vocoder


"""
This is an example of how to use a predefined Voicebox UI with a sample project.

Your run_voicebox.py can include command-line arguments with argparse,
and perform additional setup actions needed for your project.

The project needs to provide some interfaces to Voicebox to integrate with the UI.
See sample_project.py for a minimal example of those interfaces.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vc", action="store_true", help=\
            "Launches a sample voice conversion project.")
    parser.add_argument("--vocoder", action="store_true", help=\
            "Launches a sample vocoder project.")
    args = parser.parse_args()

    if args.vc:
        Sample_Project = Sample_VC_Project
        Voicebox = Voicebox_VC
        window_title = "Sample Voice Conversion Project"
    elif args.vocoder:
        Sample_Project = Sample_Vocoder_Project
        Voicebox = Voicebox_Vocoder
        window_title = "Sample Vocoder Project"
    
    # Initialize the project
    sample_project = Sample_Project()

    # Start voice conversion UI for project
    Voicebox(sample_project, window_title=window_title)
