import pygame
from star_data import star
from astronomicalObject import astronomicalObject
import random
import numpy
import cv2
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACEBLACK = (5,8,25)
LIGHTBLUE = (175, 201, 255)
LIGHTORANGE = (255, 217, 178)
STARCOLORS = [WHITE, LIGHTORANGE, LIGHTBLUE]
YELLOW = (253, 184, 19)
GRAY = (151, 151, 159)
BROWN = (195,132,42)
BLUE = (0,107,216)
TERRACOTTA = (226, 123, 88)
BRASS = (211, 156, 126)
CAMEL = (195, 161, 113)
POWDERBLUE = (213, 251, 252)
ROYALBLUE = (62, 84, 232)
CYANBLUE = (52,172,177)


# Some constants of our solar system in kg or km and the distance to the sun is in Au
SUN_MASS = 1988500 * (10 ** 24)
SUN_RADIUS = 695700

# Useful constants for converting from scientific notation
exp = 10 ** 24
# Dict that holds information about the planets
# Format is Mass, Radius of planet, Distance from SUn
planetDict = {
    'mercury' : [0.33011 * exp, 2439.7, 0.38709893],
    'venus': [4.8675 * exp, 6051.8, 0.72333199],
    'earth': [5.9724 * exp, 6371, 1],
    'mars': [0.64171 * exp, 3389.5, 1.52366231],
    'jupiter': [1,898.19 * exp, 69911, 5.20336301],
    'saturn': [568.34 * exp, 58232, 9.53707032],
    'uranus': [86.813 * exp, 25362, 19.19126393],
    'neptune': [102.413 * exp, 24622, 30.06896348],
    'pluto': [0.01303 * exp, 1188, 39.48168677]
}

screenWidth, screenHeight = 900, 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Initialize objects from the astronomicalObject class
sun = astronomicalObject(SUN_MASS, YELLOW, 20, (0, 0), 0)
mercury = astronomicalObject(planetDict['mercury'][0], GRAY, 8, (0, 0), planetDict['mercury'][2])
venus = astronomicalObject(planetDict['venus'][0], BROWN, 8, (0, 0), planetDict['venus'][2])
earth = astronomicalObject(planetDict['earth'][0], BLUE, 8, (0, 0), planetDict['earth'][0])
mars = astronomicalObject(planetDict['mars'][0], TERRACOTTA, 8, (0, 0), planetDict['mars'][0])
jupiter = astronomicalObject(planetDict['jupiter'][0], BRASS, 8, (0, 0), planetDict['jupiter'][0])
saturn = astronomicalObject(planetDict['saturn'][0], CAMEL, 8, (0, 0), planetDict['saturn'][0])
uranus = astronomicalObject(planetDict['uranus'][0], POWDERBLUE, 8, (0, 0), planetDict['uranus'][0])
neptune = astronomicalObject(planetDict['neptune'][0], ROYALBLUE, 8, (0, 0), planetDict['neptune'][0])
pluto = astronomicalObject(planetDict['pluto'][0], CYANBLUE, 8, (0, 0), planetDict['pluto'][0])


spaceObjects = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

def main():
    #starList = createStars()
    mainLoop = True
    mainSimulation = True
    image = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(image, YELLOW, (50,50), 20)

    print("For tomorrow, add some gravity. fake details abt planets except mass. make to scale version and then version that is made smaller. so calc real pos n then transform that")

    # Main loop that handles all the screens
    while mainLoop:

        # This loop handles the simulation screen
        while mainSimulation:
            clock.tick(2)
            screen.fill(SPACEBLACK)

            # Events like key presses and mouse movements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                    mainSimulation = False
            #pygame.draw.circle(screen, YELLOW, (screenWidth/2, screenHeight/2), 20)
            """pygame.draw.circle(screen, GRAY, (screenWidth / 2 + 60, screenHeight / 2), 4)
            pygame.draw.circle(screen, BROWN, (screenWidth/2 + 100, screenHeight/2), 6)
            pygame.draw.circle(screen, BLUE, (screenWidth / 2 + 140, screenHeight / 2), 8)
            pygame.draw.circle(screen, TERRACOTTA, (screenWidth / 2 + 180, screenHeight / 2), 4)
            pygame.draw.circle(screen, BRASS, (screenWidth / 2 + 220, screenHeight / 2), 14)
            pygame.draw.circle(screen, CAMEL, (screenWidth / 2 + 260, screenHeight / 2), 12)
            pygame.draw.circle(screen, POWDERBLUE, (screenWidth / 2 + 300, screenHeight / 2), 10)
            pygame.draw.circle(screen, ROYALBLUE, (screenWidth / 2 + 340, screenHeight / 2), 10)
            pygame.draw.circle(screen, CYANBLUE, (screenWidth / 2 + 380, screenHeight / 2), 2)"""
            drawSpaceObjects()
            neon_image = create_neon(image)
            #drawStars(starList)
            screen.blit(neon_image, neon_image.get_rect(center=screen.get_rect().center),
                        special_flags=pygame.BLEND_PREMULTIPLIED)
            pygame.display.update()

# Draws the planets and any other space objects
def drawSpaceObjects():
    distanceFromSunScaled = 60
    widthOrbits = 40
    for planet in spaceObjects:
        if planet != sun:
            details = planet.returnDrawDetails()
            pos = convertToNotScaleCoords(details, distanceFromSunScaled)
            pygame.draw.circle(screen, details[1], pos, details[2])
            distanceFromSunScaled += widthOrbits


def convertToNotScaleCoords(details, distanceFromSun):
    factor = distanceFromSun / details[3]
    screenWidth, screenHeight = pygame.display.get_surface().get_size()
    x = (screenWidth / 2) + (factor * details[0][0])
    y = (screenHeight / 2) +  (factor * details[0][1])
    return (x, y)





# Initializes the array of star objects
def createStars():
    # Creates an array of 100 elements
    starList = [0] * 300
    chanceOfMovingStars = 5
    chanceOfFlickering = 5
    screenWidth, screenHeight = pygame.display.get_surface().get_size()
    for x in range(len(starList)):
        # Some parameters for the stars
        posX = random.randint(0, 2000)
        posY = random.randint(0, 2000)
        size = random.randint(0,2)
        color = random.choice(STARCOLORS)
        flicker = False
        # These next two if statements allow a chance for the stars to flicker or move
        if random.randint(0,100) < chanceOfFlickering:
            flicker = True
        speedX = 0
        speedY = 0
        if random.randint(0,100) < chanceOfMovingStars:
            speedX = random.randint(-50,50) / 100
            speedY = random.randint(-50,50) / 100
        starList[x] = star([posX, posY], size, color, flicker, [speedX, speedY])

    return starList

# Draws the stars based on the properties from the star_data class
def drawStars(starList):
    for x in range(len(starList)):
        pos = starList[x].returnPos()
        size = starList[x].returnSize()
        color = starList[x].returnColor()
        pygame.draw.circle(screen, color, (pos[0], pos[1]), size)

# This helps to create a glow around the objects that make them look a bit more pleasant to the eyes
def create_neon(surf):
    surf_alpha = surf.convert_alpha()
    rgb = pygame.surfarray.array3d(surf_alpha)
    alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    image = numpy.concatenate((rgb, alpha), 2)
    cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
    cv2.blur(image, ksize=(5, 5), dst=image)
    bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    return bloom_surf

main()
