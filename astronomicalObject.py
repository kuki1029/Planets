import math
import random

class astronomicalObject:

    convertAUtoKM = 1.496 * (10 ** 8)
    convertAUtoPixel = 100              # 1 Au = 100 Px
    # Constructor
    # Mass is in kg
    # Size is in km and is the radius of the object
    # Speed will be in m/s
    # InitialPosition is the distance from the sun in Au
    def __init__(self, mass, color, size, initialSpeed, initialPos):
        self.mass = mass
        self.color = color
        self.size = size
        self.initialSpeed = initialSpeed

        # Decides the position of the object relative to the sun.
        # Randomly assigns an angle
        hyp = initialPos
        angle = math.radians(random.randint(0,360))
        posX = math.cos(angle) * hyp
        posY = math.sin(angle) * hyp
        self.distance = initialPos
        self.pos = [posX, posY]



    def returnDrawDetails(self):
        return [self.pos, self.color, self.size, self.distance]



    # This function will convert all our values to x and y values that can be drawn relative to the sun
    def convertToCoords(self):
        pass


