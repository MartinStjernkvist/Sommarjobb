"""This file acts as the main module for this script."""

"""This file acts as the main module for this script."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parameters import *

import traceback
import adsk.core
import adsk.fusion
# import adsk.cam

# Initialize the global variables for the Application and UserInterface objects.
app = adsk.core.Application.get()
ui  = app.userInterface


def run(_context: str):
    """This function is called by Fusion when the script is run."""

    try:
        # Your code goes here.
        ui.messageBox(f'"{app.activeDocument.name}" is the active Document.')
    except:  #pylint:disable=bare-except
        # Write the error message to the TEXT COMMANDS window.
        app.log(f'Failed:\n{traceback.format_exc()}')
