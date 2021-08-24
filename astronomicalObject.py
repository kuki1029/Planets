import math
import random
import pygame

class astronomicalObject:

    convertAUtoM = 1.496 * (10 ** 11)
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
        self.vel = initialSpeed

        # Decides the position of the object relative to the sun.
        # Randomly assigns an angle
        hyp = initialPos
        angle = math.radians(random.randint(0,360))
        posX = math.cos(angle) * hyp
        posY = math.sin(angle) * hyp
        self.distance = initialPos
        self.pos = [posX, posY]
        #print(str(self.pos[0]) + ", " + str(self.pos[1]))


    def calculateChangeInPos(self, force):
        accelX = force[0] / self.mass
        accelY = force[1] / self.mass
        #print(str(force[0]) + ", " + str(force[1]))
        #print("S")
        #print(str(self.pos[0]) + ", " + str(self.pos[1]))
        self.vel[0] += (accelX / self.convertAUtoM) * 10000
        self.vel[1] += (accelY / self.convertAUtoM) * 10000
        self.pos[0] = self.pos[0] + (self.vel[0] * 10000)- ((0.5 * (accelX / self.convertAUtoM)) * 100000000)
        self.pos[1] = self.pos[1] + (self.vel[1] * 10000 )- ((0.5 * (accelY / self.convertAUtoM)) * 100000000)
        #print(str(self.pos[0]) + ", " + str(self.pos[1]))
        #print(str(self.vel[0]) + ", " + str(self.vel[1]))

    # Returns the details needed to draw the objects
    def returnDrawDetails(self):
        return [self.pos, self.color, self.size, self.distance]

    # Returns the coordinates of the object
    def returnCoords(self):
        return self.pos

    # Calculates and returns the angles of the object relative to the x axis in degrees
    def returnAngle(self):
        angle = math.degrees(math.atan2(self.pos[1], self.pos[0]))
        if angle < 0:
            angle = angle + 360
        return angle

    # Returns the distance from the sun in Au
    def returnDistance(self):
        return self.distance

    # Returns the mass in kg
    def returnMass(self):
        return self.mass




