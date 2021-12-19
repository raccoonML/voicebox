from voicebox.vc import Voicebox
from sample_project import Sample_Project


"""
This is an example of how to use a predefined Voicebox UI with a sample project.

Your run_voicebox.py can include command-line arguments with argparse,
and perform additional setup actions needed for your project.

The project needs to provide some interfaces to Voicebox to integrate with the UI.
See sample_project.py for a minimal example of those interfaces.
"""

if __name__ == '__main__':
    # Initialize the project
    sample_project = Sample_Project()

    # Start voice conversion UI for project
    Voicebox(sample_project, window_title="Sample Project")
