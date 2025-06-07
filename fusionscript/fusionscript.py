"""This file acts as the main module for this script."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parameters import *
from imports import *


import traceback
import adsk.core
import adsk.fusion
# import adsk.cam

'''
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
'''

def run(context):
    try:
        # Get the application and active design
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('No active Fusion 360 design found.', 'Error')
            return

        # Get the root component
        rootComp = design.rootComponent

        # Create a new sketch on the XY plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Parameters for the sinusoidal curve
        amplitude = 1.0  # Amplitude in centimeters
        frequency = 1.0  # Frequency (cycles per centimeter)
        length = 10.0    # Length of the curve along x-axis in centimeters
        numPoints = 100  # Number of points to define the spline

        # Generate points for the sinusoidal curve
        points = adsk.core.ObjectCollection.create()
        for i in range(numPoints + 1):
            x = (i / numPoints) * length
            y = amplitude * math.sin(frequency * 2 * math.pi * x)
            z = 0.0
            points.add(adsk.core.Point3D.create(x, y, z))

        # Create a spline through the points
        sketch.sketchCurves.sketchFittedSplines.add(points)

        # Create an extrusion to form a surface
        profile = sketch.profiles.item(0)  # Get the first profile
        extrudes = rootComp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(0.1)  # Thin surface (0.1 cm)
        extrudeInput.setDistanceExtent(False, distance)
        extrude = extrudes.add(extrudeInput)

        ui.messageBox('Sinusoidal line and surface created successfully.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))