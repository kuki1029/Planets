import random
# This class stores the stars and allows them to flicker as time goes on
class star:

    # Constructor
    # flicker tells us at what rate the star needs to flicker and how big it gets
    # Speed tells us if the star is going to be moving in the background
    def __init__(self, pos, size, color, flicker, speed):
        self.pos = pos
        self.size = size
        self.color = color
        self.flicker = flicker
        self.speed = speed
        self.clockCount = 0



    # Returns position and changes it based on the speed
    def returnPos(self):
        if self.clockCount > 100:
            self.pos[0] += self.speed[0]
            self.pos[1] += self.speed[1]
            self.clockCount = 0
        self.clockCount += 1
        return self.pos

    # Returns size and update the size based on flicker property
    def returnSize(self):
        if self.clockCount > 100:
            if self.flicker and random.randint(0,100) > 60:
                if self.size >= 3:
                    self.size = 1
                else:
                    self.size += 1
            self.clockCount = 0
        self.clockCount += 1
        return self.size



    # Returns color
    def returnColor(self):
        return self.color
