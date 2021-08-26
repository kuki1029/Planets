import math
import random

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
        self.assignRandomStart(initialPos)
        self.vel = self.calcVelComponent(initialSpeed)



    # Decides the position of the object relative to the sun.
    # Randomly assigns an angle
    def assignRandomStart(self, initialPos):
        hyp = initialPos
        angle = math.radians(random.randint(0, 360))
        posX = math.cos(angle) * hyp
        posY = math.sin(angle) * hyp
        self.distance = initialPos
        self.pos = [posX, posY]

    # Returnrs the components of the velocity
    def calcVelComponent(self, vel):
        velX, velY = 0, 0
        angle = math.radians(self.returnAngle() + 90)
        velX = (-1 * (math.cos(angle) * vel)) / self.convertAUtoM
        velY = (-1 * (math.sin(angle) * vel)) / self.convertAUtoM
        print(velX, velY)
        return [velX, velY]


    # Calculates how the force will effect the position
    # Force is in newtons
    def calculateChangeInPos(self, force):
        accelX = (force[0] / self.mass) / self.convertAUtoM
        accelY = (force[1] / self.mass) / self.convertAUtoM
        time = 10000
        # Formulas for velocity and distance used here by Newton
        self.vel[0] += accelX * time
        self.vel[1] += accelY * time

        self.pos[0] = self.pos[0] + (self.vel[0] * time) - ((0.5 * accelX) * (time ** 2))
        self.pos[1] = self.pos[1] + (self.vel[1] * time) - ((0.5 * accelY) * (time ** 2))


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




