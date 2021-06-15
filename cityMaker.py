# Procedural City Maker
import maya.cmds as cmds
import random
from functools import partial
if not cmds.commandPort(":4434", query=True):
    cmds.commandPort(name=":4434")


class Building(object):
    """Parent Building class"""

    def __init__(self, width, height):
        self.height = height
        self.width = width

    def info(self):
        """Print information about the building"""
        print("Width: %s\nHeight: %s" % (self.width, self.height))

    def move_building(self, x, y, z):
        """Move method to place building in correct position"""
        cmds.move(x, y, z)

    def add_antenna(self, x, y, z):
        """Add cone-shaped antenna to building"""
        antenna = cmds.polyCone(r=.2, h=2)
        cmds.move(x, y, z)


class CubeBuilding(Building):
    """Child class: polycube building"""

    def __init__(self, width, height):
        super(CubeBuilding, self).__init__(width, height)
        self.polyCube = cmds.polyCube(w=self.width, d=self.width, h=self.height)


class CylinderBuilding(Building):
    """Child class: cylinder building"""

    def __init__(self, width, height, subdivisions):
        super(CylinderBuilding, self).__init__(width, height)
        self.subdivisions = subdivisions
        self.polyCylinder = cmds.polyCylinder(radius=self.width/2, h=self.height, sx=self.subdivisions)

    def info(self):
        """Print additional information (subdivisions)"""
        super(CylinderBuilding, self).info()
        print("Subdivisions: %s\n" % (self.subdivisions))


class CityMakerOptions:
    def __init__(
        self,
        minHeight=0,
        maxHeight=20,
        buildingGap=0,
        xDim=20,
        yDim=20,
        cylinderOption=False,
        antennaOption=False
    ):
        self.minHeight = minHeight
        self.maxHeight = maxHeight
        self.buildingGap = buildingGap
        self.xDim = xDim
        self.yDim = yDim
        self.cylinderOption = cylinderOption
        self.antennaOption = antennaOption


class CityMaker:
    """Class with main logic to create cities"""
    def __init__(self,  options):
        self.options = options
        self.buildings = []

    def generate(self, *_):

            # Set polyplane for ground level
            cmds.polyPlane(width=self.options.xDim, height=self.options.yDim)
            cmds.move(self.options.xDim/2, 0, self.options.yDim/2)

            x = 0

            # Nested while loop to create grid of buildings
            while x < self.options.xDim:
                z = 0
                while z < self.options.yDim:
                    # Get random height within range
                    height = random.randrange(self.options.minHeight, self.options.maxHeight)

                    # Choice of building type, accounting for if cylinder checkbox is checked
                    if self.options.cylinderOption == 1:
                        buildingType = random.randrange(0, 10)
                    else:
                        buildingType = 1

                    buildingWidth = random.randrange(1, 3)

                    if buildingType < 8:
                        # PolyCube option
                        cube = CubeBuilding(buildingWidth, height)
                        cube.move_building(x + buildingWidth//2 + self.options.buildingGap, height//2, z + buildingWidth//2 + self.options.buildingGap)

                        if self.options.antennaOption == 1:
                            # Antenna option
                            isAntenna = random.randrange(0, 10)
                            if isAntenna < 2:
                                cube.add_antenna(x + buildingWidth//2 + self.options.buildingGap, height, z + buildingWidth//2 + self.options.buildingGap)
                        self.buildings.append(cube)

                    else:
                        # Cylinder option
                        subdiv = random.randrange(3, 12)
                        cylinder = CylinderBuilding(buildingWidth, height, subdiv)
                        cylinder.move_building(x + buildingWidth//2 + self.options.buildingGap, height//2, z + buildingWidth//2 + self.options.buildingGap)
                        self.buildings.append(cylinder)

                    z += buildingWidth + self.options.buildingGap
                x += buildingWidth + self.options.buildingGap

    # Demolish the city
    def delete(self, *_):
        allObjects = cmds.ls("pCube*", "pPlane*", "pCylinder*", "pCone*")
        for object in allObjects:
            cmds.delete(object)


class CityMakerUI(object):
    """ Class in charge of UI layout"""
    def __init__(self, windowID="myWindowID"):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

        self.window_id = cmds.window(windowID, title="City Maker", sizeable=False, resizeToFitChildren=True)
        self.layout = cmds.columnLayout(columnAttach=('both', 5), rowSpacing=10, columnWidth=400, parent=self.window_id)

        # Slider groups for height and building gap
        self.minHeight = cmds.intSliderGrp(label="Minimum Height", min=0, max=20, value=0, field=True)
        self.maxHeight = cmds.intSliderGrp(label="Maximum Height", min=0, max=20, value=20, field=True)
        self.buildingGap = cmds.floatSliderGrp(label="Building Gap", min=0, max=1, value=0, field=True)

        # Text fields for city X and Y dimensions
        cmds.text(label="X Dimension")
        self.xDim = cmds.textField(tx=20)

        cmds.text(label="Y Dimension")
        self.yDim = cmds.textField(tx=20)

        # Checkboxes for presence of cylinders and antennas
        self.cylinderOption = cmds.checkBox(label="Cylinders", value=False, onc="cylinderOption=1", ofc="cylinderOption=0")
        self.antennaOption = cmds.checkBox(label="Antennas", value=False, onc="antennaOption=1", ofc="antennaOption=0")

        city_maker = CityMaker(self.get_user_options())
        cmds.button(label="Generate City", command=self.generate_button_handler)
        cmds.button(label="Demolish City", command=city_maker.delete)

        # Show window
        cmds.showWindow(self.window_id)

    # Handler for when generate button is pressed
    def generate_button_handler(self, *_):
        # Update city_maker variable with current CityMakerOptions
        city_maker = CityMaker(self.get_user_options())
        city_maker.generate()

    def get_user_options(self):
        return CityMakerOptions(
            minHeight=int(cmds.intSliderGrp(self.minHeight, q=True, value=True)),
            maxHeight=int(cmds.intSliderGrp(self.maxHeight, q=True, value=True)),
            buildingGap=int(cmds.floatSliderGrp(self.buildingGap, q=True, value=True)),
            xDim=int(cmds.textField(self.xDim, q=True, text=True)),
            yDim=int(cmds.textField(self.yDim, q=True, text=True)),
            cylinderOption=int(cmds.checkBox(self.cylinderOption, q=True, value=True)),
            antennaOption=int(cmds.checkBox(self.antennaOption, q=True, value=True))
        )

# Main Execution
ui = CityMakerUI("myWindowID")
