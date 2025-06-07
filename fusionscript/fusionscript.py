"""This file acts as the main module for this script."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parameters import *
import math


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
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent
        
        # Get input from user
        amplitude, cancelled = ui.inputBox('Enter amplitude (cm):', 'Sine Wave Parameters', '2.0')
        if cancelled:
            return
        
        frequency, cancelled = ui.inputBox('Enter frequency (cycles):', 'Sine Wave Parameters', '2.0')
        if cancelled:
            return
            
        length, cancelled = ui.inputBox('Enter length (cm):', 'Sine Wave Parameters', '10.0')
        if cancelled:
            return
        
        # Convert strings to numbers
        try:
            amplitude = float(amplitude)
            frequency = float(frequency)
            length = float(length)
        except:
            ui.messageBox('Invalid input. Please enter numeric values.')
            return
        
        # Create or update sketch
        sketch = None
        sketchName = 'InteractiveSineWave'
        
        # Check if sketch already exists
        for sk in rootComp.sketches:
            if sk.name == sketchName:
                sketch = sk
                # Clear existing curves
                sketch.sketchCurves.sketchFittedSplines.clear()
                break
        
        # Create new sketch if it doesn't exist
        if not sketch:
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            sketch.name = sketchName
        
        # Generate points for the sine curve
        resolution = 100
        points = adsk.core.ObjectCollection.create()
        
        for i in range(resolution + 1):
            x = (i / resolution) * length
            y = amplitude * math.sin(2 * math.pi * frequency * x / length)
            z = 0
            
            point = adsk.core.Point3D.create(x, y, z)
            points.add(point)
        
        # Create spline through points
        splines = sketch.sketchCurves.sketchFittedSplines
        spline = splines.add(points)
        
        # Fit the view to show the entire curve
        app.activeViewport.fit()
        
        ui.messageBox(f'Sine wave created with:\nAmplitude: {amplitude} cm\nFrequency: {frequency} cycles\nLength: {length} cm')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def createSurfaceFromSineWave():
    """Create a surface by extruding or lofting the sine wave"""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent
        
        # Find the sine wave sketch
        sketch = None
        for sk in rootComp.sketches:
            if 'SineWave' in sk.name:
                sketch = sk
                break
        
        if not sketch:
            ui.messageBox('Sine wave sketch not found. Please create one first.')
            return
        
        # Create extrude feature
        profiles = adsk.core.ObjectCollection.create()
        
        # For curves, we need to create a surface by extruding or using other surface tools
        # Since splines can't be directly extruded, we'll create a loft or sweep
        
        # Get the spline curve
        if sketch.sketchCurves.sketchFittedSplines.count > 0:
            spline = sketch.sketchCurves.sketchFittedSplines.item(0)
            
            # Create a simple extrude by creating a second sketch
            # Create another sketch parallel to the first
            planes = rootComp.constructionPlanes
            planeInput = planes.createInput()
            
            # Create a plane offset from XY plane
            planeInput.setByOffset(rootComp.xYConstructionPlane, adsk.core.ValueInput.createByReal(2.0))
            offsetPlane = planes.add(planeInput)
            
            # Create second sketch on offset plane
            sketch2 = rootComp.sketches.add(offsetPlane)
            
            # Copy the sine curve to the new sketch (simplified approach)
            points2 = adsk.core.ObjectCollection.create()
            for i in range(101):
                x = (i / 100.0) * 10.0  # Use same parameters as original
                y = 2.0 * math.sin(2 * math.pi * 2.0 * x / 10.0)
                z = 0
                
                point = adsk.core.Point3D.create(x, y, z)
                points2.add(point)
            
            spline2 = sketch2.sketchCurves.sketchFittedSplines.add(points2)
            
            # Create loft between the two curves
            lofts = rootComp.features.loftFeatures
            loftInput = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            
            # Add profiles (the curves)
            loftSections = loftInput.loftSections
            loftSections.add(spline)
            loftSections.add(spline2)
            
            # Create the loft
            loft = lofts.add(loftInput)
            
            ui.messageBox('Surface created from sine wave!')
        
    except:
        if ui:
            ui.messageBox('Failed to create surface:\n{}'.format(traceback.format_exc()))