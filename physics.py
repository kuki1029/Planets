
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
        angle = math.radians(angle)
        distance = distance * self.convertAUtoM
        force = (self.gravConstant * mass1 * mass2) / (distance ** 2)
        forceX = force * math.cos(angle) * -1
        forceY = force * math.sin(angle) * -1

        return [forceX, forceY]

    def orbitVelocity(self, mass, distance):
        distance = distance * self.convertAUtoM
        return (math.sqrt((self.gravConstant * mass) / distance))


