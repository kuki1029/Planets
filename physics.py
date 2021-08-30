
# All physics calculations are done here
import math


class physicsCalc:
    convertAUtoM = 1.496 * (10 ** 11)
    gravConstant = 6.67 * (10 ** (-11))

    # Constructor
    # Mass is in kg and distance in km
    def __init__(self, solarSystem):
        # We set these parameters to 1 as we aren't dealing with real world scales for the gravity simulation
        # These modified numbers allow for faster processing and makes it easier for the user to play around with the objects
        if not solarSystem:
            self.convertAUtoM = 1
            self.gravConstant = 1

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


