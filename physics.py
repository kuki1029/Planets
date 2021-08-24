
# All physics calculations are done here
import math


class physicsCalc:
    convertAUtoM = 1.496 * (10 ** 11)
    gravConstant = 6.67 * (10 ** (-11))
    # Constructor
    # Mass is in kg and distance in km
    def __init__(self):
        pass

    # Calculates the x and y component of the force between two planets
    def gravForce(self, mass1, mass2, distance, angle):
        distance = distance * self.convertAUtoM
        force = (self.gravConstant * mass1 * mass2) / (distance ** 2)
        forceX = force * math.cos(math.radians(angle)) * -1
        forceY = force * math.sin(math.radians(angle)) * -1
        #print(force)
        #print("angle" + str(angle))
        #print("force:" + str([forceX, forceY]))
        return [forceX, forceY]

