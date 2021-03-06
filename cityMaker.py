# Procedural City Maker

import maya.cmds as cmds
import random
from functools import partial

def createUI():
    
    windowID = "myWindowID"
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    window = cmds.window(windowID, title="City Maker", sizeable=False, resizeToFitChildren=True)        
    cmds.columnLayout(columnAttach=('both', 5), rowSpacing=10, columnWidth=400)

    minHeight = cmds.intSliderGrp(label="Minimum Height", min=0, max=20, value=0, field=True)
    maxHeight = cmds.intSliderGrp(label="Maximum Height", min=0, max=20, value=20, field=True)
    buildingGap = cmds.floatSliderGrp(label="Building Gap", min=0, max=1, value=0, field=True)    

    
    cmds.text(label="X Dimension")
    xDim = cmds.textField(tx = 20)
    
    cmds.text(label="Y Dimension")
    yDim = cmds.textField(tx = 20)
        
    cylinderOption = cmds.checkBox(label="Cylinders", value=False, onc="cylinderOption=1", ofc="cylinderOption=0")
    antennaOption = cmds.checkBox(label="Antennas", value=False, onc="antennaOption=1", ofc="antennaOption=0")
    

    cmds.button(label = "Generate City", command = partial(generate, minHeight, maxHeight, buildingGap, xDim, yDim, cylinderOption, antennaOption))
    cmds.button(label = "Demolish City", command = partial(delete))
    
    
     # Show window
    cmds.showWindow(window)
    
def generate(minHeight, maxHeight, buildingGap, xDim, yDim, cylinderOption, antennaOption, *args):
        
    minHeight = int(cmds.intSliderGrp(minHeight, q=True, value=True))
    maxHeight = int(cmds.intSliderGrp(maxHeight, q=True, value=True))
    buildingGap = int(cmds.floatSliderGrp(buildingGap, q=True, value=True))
    xDim = int(cmds.textField(xDim, q=True, text=True))
    yDim = int(cmds.textField(yDim, q=True, text=True))
    cylinderOption = int(cmds.checkBox(cylinderOption, q=True, value=True))
    antennaOption = int(cmds.checkBox(antennaOption, q=True, value=True))
   
    # Set polyplane
    # cmds.polyPlane(width = xDim, height = yDim)
    # cmds.move(xDim/2, 0, yDim/2)
    
    x = 0
    
    while x < xDim:
        z = 0
        while z < yDim:
            # Get random height within range
            height = random.randrange(minHeight, maxHeight)
            
            # Choice of building type, accounting for if cylinder checkbox is checked
            if cylinderOption == 1:
                buildingType = random.randrange(0, 10)
            else:
                buildingType = 1
	
            buildingWidth = random.randrange(1, 3)            

            if buildingType > 0 and buildingType < 9:
                # PolyCube option
                cube = cmds.polyCube(w = buildingWidth, d = buildingWidth, h = height)
                cmds.move(x + buildingWidth/2 + buildingGap, height/2, z + buildingWidth/2 + buildingGap)
                

                if antennaOption == 1:
                    # Antenna option
                    isAntenna = random.randrange(0, 10)
                    if isAntenna < 2:
                        antenna = cmds.polyCone(r=.2, h = 2)
                        cmds.move(x + buildingWidth/2 + buildingGap, height, z + buildingWidth/2 + buildingGap)

            else:
                # Cylinder option
                subdiv = random.randrange(3, 12)
                polyCylinder = cmds.polyCylinder(radius=buildingWidth/2, h = height, sx = subdiv)
                cmds.move(x + buildingWidth/2 + buildingGap, height/2, z + buildingWidth/2 + buildingGap)
            z += buildingWidth + buildingGap
        x += buildingWidth + buildingGap

# Demolish the city
def delete(*args):
    allObjects = cmds.ls("pCube*", "pPlane1", "pCylinder*", "pCone*")
    for object in allObjects:
        cmds.delete(object)
    
createUI()
