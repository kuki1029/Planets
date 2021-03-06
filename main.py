import math

import pygame
from star_data import star
from astronomicalObject import astronomicalObject
from physics import physicsCalc
import random
import numpy
import cv2

pygame.init()
pygame.font.init()
fontMenu = pygame.font.SysFont('segoeui', 50)
font = pygame.font.SysFont('segoeui', 35)
fontSmall = pygame.font.SysFont('segoeui', 20)
pygame.display.set_caption("Physics Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKPURPLE = (34, 28, 52)
LIGHTGRAY = (232, 228, 236)
SPACEBLACK = (5, 8, 25)
LIGHTBLUE = (175, 201, 255)
LIGHTORANGE = (255, 217, 178)
STARCOLORS = [WHITE, LIGHTORANGE, LIGHTBLUE]
YELLOW = (253, 184, 19)
GRAY = (151, 151, 159)
BROWN = (195, 132, 42)
BLUE = (0, 107, 216)
TERRACOTTA = (226, 123, 88)
BRASS = (211, 156, 126)
CAMEL = (195, 161, 113)
POWDERBLUE = (213, 251, 252)
ROYALBLUE = (62, 84, 232)
CYANBLUE = (52, 172, 177)
RED = (176,64,64)

# Some constants of our solar system in kg or km and the distance to the sun is in Au
SUN_MASS = 1988500 * (10 ** 24)
SUN_RADIUS = 695700
gravConstant = 6.67 * (10 ** (-11))

# Object from the physics class
physicsSolarSimCalculator = physicsCalc(True)
physicsObjectsCalc = physicsCalc(False)

# Useful constants for converting from scientific notation
exp = 10 ** 24
# Dict that holds information about the planets
# Format is Mass, Radius of planet, Distance from SUn
planetDict = {
    'mercury': [0.33011 * exp, 2439.7, 0.38709893],
    'venus': [4.8675 * exp, 6051.8, 0.72333199],
    'earth': [5.9724 * exp, 6371, 1],
    'mars': [0.64171 * exp, 3389.5, 1.52366231],
    'jupiter': [1898.19 * exp, 69911, 5.20336301],
    'saturn': [568.34 * exp, 58232, 9.53707032],
    'uranus': [86.813 * exp, 25362, 19.19126393],
    'neptune': [102.413 * exp, 24622, 30.06896348],
    'pluto': [0.01303 * exp, 1188, 39.48168677]
}

screenWidth, screenHeight = 900, 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Calculates the orbital speed for all the planets
orbitalVel = []
for planet in planetDict:
    orbitalVel.append(physicsSolarSimCalculator.orbitVelocity(SUN_MASS, planetDict[planet][2]))

# Initialize objects from the astronomicalObject class
sun = astronomicalObject(SUN_MASS, YELLOW, 20, 0, 0, True)
mercury = astronomicalObject(planetDict['mercury'][0], GRAY, 8, orbitalVel[0], planetDict['mercury'][2], True)
venus = astronomicalObject(planetDict['venus'][0], BROWN, 8, orbitalVel[1], planetDict['venus'][2], True)
earth = astronomicalObject(planetDict['earth'][0], BLUE, 8, orbitalVel[2], planetDict['earth'][2], True)
mars = astronomicalObject(planetDict['mars'][0], TERRACOTTA, 8, orbitalVel[3], planetDict['mars'][2], True)
jupiter = astronomicalObject(planetDict['jupiter'][0], BRASS, 8, orbitalVel[4], planetDict['jupiter'][2], True)
saturn = astronomicalObject(planetDict['saturn'][0], CAMEL, 8, orbitalVel[5], planetDict['saturn'][2], True)
uranus = astronomicalObject(planetDict['uranus'][0], POWDERBLUE, 8, orbitalVel[6], planetDict['uranus'][2], True)
neptune = astronomicalObject(planetDict['neptune'][0], ROYALBLUE, 8, orbitalVel[7], planetDict['neptune'][2], True)
pluto = astronomicalObject(planetDict['pluto'][0], CYANBLUE, 8, orbitalVel[8], planetDict['pluto'][2], True)

# List of all the planetary objects
spaceObjects = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

def main():
    starList = createStars()

    # Variables that control the screen loops
    mainLoop = True
    SolarSystemSimulationScreen = False
    gravitySimulation = True
    menuScreen = False
    secondMenuScreen = False
    creditScreen = False
    helpScreen = False

    counter = 0

    # Makes the glow effect around sun
    image = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(image, YELLOW, (50, 50), 20)

    # Main loop that handles all the screens
    while mainLoop:
        # This loop handles the simulation screen
        counter = 0
        while SolarSystemSimulationScreen:
            clock.tick(100)
            screen.fill(SPACEBLACK)

            # Events like key presses and mouseHeld movements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                    SolarSystemSimulationScreen = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        SolarSystemSimulationScreen = False
                        menuScreen = True

            drawSpaceObjects()
            calculateForces()

            if counter < 500:
                textSurface = fontSmall.render("Press Esc to go back", True, LIGHTGRAY)
                screen.blit(textSurface, (0, 0))
                counter += 1


            # Creates glow effect around sun
            neon_image = create_neon(image)
            screen.blit(neon_image, neon_image.get_rect(center=screen.get_rect().center),
                        special_flags=pygame.BLEND_PREMULTIPLIED)
            pygame.display.update()


        # Loop that handles the gravity simulations
        counter = 0
        sizeObject = 1
        density = 10
        userCreatedObjects = [astronomicalObject(100000, RED, 30, [0, 0], [0, 0], False)]
        mouseHeld = False
        color = WHITE
        while gravitySimulation:
            x, y = pygame.mouse.get_pos()
            clock.tick(100)
            screen.fill(SPACEBLACK)
            dx, dy = 0, 0
            screen_width, screen_height = pygame.display.get_surface().get_size()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                    gravitySimulation = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gravitySimulation = False
                        menuScreen = True
                    # If the number keys are pressed, it makes the created objects more heavy
                    elif event.key == pygame.K_1:
                        density = 10
                        color = WHITE
                    elif event.key == pygame.K_2:
                        density = 20
                        color = RED
                    elif event.key == pygame.K_3:
                        density = 50
                        color = CYANBLUE
                # Gives us the speed of the mouseHeld relative to its last position
                if mouseHeld and event.type == pygame.MOUSEMOTION:
                    dx, dy = event.rel
                # Creates a new object from the astronomical object class when the user is no longer clicking the mouseHeld
                if event.type == pygame.MOUSEBUTTONUP:
                    distanceX = (x - (screen_width/2))
                    distanceY = (y - (screen_height/2))
                    userCreatedObjects.append(astronomicalObject(sizeObject * density, color, sizeObject, [dx, dy], [distanceX, distanceY], False))

            # IF user if holding down the mouseHeld, it creates a circle on the screen
            click = pygame.mouse.get_pressed()
            if click[0]:
                sizeObject += 0.5
                mouseHeld = True
            if not click[0]:
                sizeObject = 0.5
                mouseHeld = False

            # IF the mouseHeld is held, a circle is created
            if mouseHeld:
                pygame.draw.circle(screen, color, [x, y], sizeObject)
            drawUserObjects(userCreatedObjects)
            calculateUserObjectForce(userCreatedObjects)
            pygame.display.update()


        # This loops holds the code for the menu screen
        counter = 0
        while menuScreen:
            screen.fill(SPACEBLACK)
            clock.tick(100)
            # Variables needed to detect if the mouseHeld is within the buttons
            buttonWidth = 300
            buttonLength = 80
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]
            screen_width, screen_height = pygame.display.get_surface().get_size()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                    menuScreen = False
                # Checks if the mouseHeld is within the buttons
                elif event.type == pygame.MOUSEBUTTONUP:
                    if (screen_width / 2 - (buttonWidth / 2)) < x < (screen_width / 2 - (buttonWidth / 2) + buttonWidth):
                        if ((screen_height / 2) - 100) < y < ((screen_height / 2) - 100 + buttonLength):
                            menuScreen = False
                            secondMenuScreen = True
                        elif (screen_height / 2) < y < ((screen_height / 2) + buttonLength):
                            menuScreen = False
                            creditScreen = True
                        elif ((screen_height / 2) + 100) < y < ((screen_height / 2) + 100 + buttonLength):
                            menuScreen = False
                            helpScreen = True


            drawStars(starList)
            drawMenu()
            pygame.display.update()

        counter = 0
        # Displays the second menu screen with more detailed options
        while secondMenuScreen:
            screen.fill(SPACEBLACK)
            clock.tick(100)
            # Variables needed to detect if the mouseHeld is within the buttons
            buttonWidth = 300
            buttonLength = 80
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]
            screen_width, screen_height = pygame.display.get_surface().get_size()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                    secondMenuScreen = False
                # Checks if the mouseHeld is within the buttons
                elif event.type == pygame.MOUSEBUTTONUP:
                    if (screen_width / 2 - (buttonWidth / 2)) < x < (screen_width / 2 - (buttonWidth / 2) + buttonWidth):
                        if ((screen_height / 2) - 100) < y < ((screen_height / 2) - 100 + buttonLength):
                            secondMenuScreen = False
                            SolarSystemSimulationScreen = True
                        elif (screen_height / 2) < y < ((screen_height / 2) + buttonLength):
                            secondMenuScreen = False
                            gravitySimulation = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        secondMenuScreen = False
                        menuScreen = True

            if counter < 500:
                textSurface = fontSmall.render("Press Esc to go back", True, LIGHTGRAY)
                screen.blit(textSurface, (0, 0))
                counter += 1

            drawStars(starList)
            drawSecondMenu()
            pygame.display.update()

        while creditScreen:
            pass

        while helpScreen:
            pass


# Draws the planets and any other space objects
def drawSpaceObjects():
    # This is the number of pixels between the orbits
    distanceFromSunScaled = 60
    widthOrbits = 40
    for planet in spaceObjects:
        # Draws the planets except the sun as we already drew it above
        if planet != sun:
            details = planet.returnDrawDetails()
            pos = convertToNotScaleCoords(details, distanceFromSunScaled)
            pygame.draw.circle(screen, details[1], pos, details[2])
            distanceFromSunScaled += widthOrbits


# Converts the Au distances to pixel values that are scaled to be easier to view on screen
def convertToNotScaleCoords(details, distanceFromSun):
    factor = distanceFromSun / details[3]
    screenWidth, screenHeight = pygame.display.get_surface().get_size()
    x = (screenWidth / 2) + (factor * details[0][0])
    y = (screenHeight / 2) + (factor * details[0][1])
    return (x, y)

# Draws objects created by the user
def drawUserObjects(userCreatedObjects):
    for object in userCreatedObjects:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        details = object.returnDrawDetails()
        # Finds appropraite coordinates relative to the center of the screen
        x = details[0][0] + (screenWidth / 2)
        y = details[0][1] + (screenHeight / 2)
        pygame.draw.circle(screen, details[1], (x, y), details[2])

# Calculates force for the user created objects
def calculateUserObjectForce(userCreatedObjects):
    for mainObject in userCreatedObjects:
        forceX = 0
        forceY = 0
        x, y = mainObject.returnCoords()
        angle = mainObject.returnAngle()
        for object in userCreatedObjects:
            x2, y2 = object.returnCoords()
            distance = math.sqrt(((x - x2) ** 2) + ((y - y2) ** 2))
            if object != mainObject:
                force = physicsObjectsCalc.gravForce(mainObject.returnMass(), object.returnMass(), distance, angle)
                forceX += force[0]
                forceY += force[1]
        mainObject.calculateChangeInPos([forceX, forceY])


# Calculates forces for each of the planets
def calculateForces():
    for mainPlanet in spaceObjects:
        if mainPlanet != sun:
            forceX = 0
            forceY = 0
            x, y = mainPlanet.returnCoords()
            angle = mainPlanet.returnAngle()
            for planet in spaceObjects:
                x2, y2 = planet.returnCoords()
                distance = math.sqrt( ((x - x2) ** 2) + ((y - y2) ** 2))
                if planet != mainPlanet:
                    force = physicsSolarSimCalculator.gravForce(mainPlanet.returnMass(), planet.returnMass(), distance, angle)
                    forceX += force[0]
                    forceY += force[1]
            mainPlanet.calculateChangeInPos([forceX, forceY])


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
        size = random.randint(0, 2)
        color = random.choice(STARCOLORS)
        flicker = False
        # These next two if statements allow a chance for the stars to flicker or move
        if random.randint(0, 100) < chanceOfFlickering:
            flicker = True
        speedX = 0
        speedY = 0
        if random.randint(0, 100) < chanceOfMovingStars:
            speedX = random.randint(-50, 50) / 100
            speedY = random.randint(-50, 50) / 100
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


# Draws the menu buttons
def drawMenu():
    buttonWidth = 300
    buttonLength = 80
    pos = pygame.mouse.get_pos()
    x, y = pos[0], pos[1]
    screen_width, screen_height = pygame.display.get_surface().get_size()
    startButton = False
    help = False
    credits = False

    # Checks where the mouse is and enables the corresponding buttons
    if (screen_width / 2 - (buttonWidth / 2)) < x < (screen_width / 2 - (buttonWidth / 2) + buttonWidth):
        if ((screen_height / 2) - 100) < y < ((screen_height / 2) - 100 + buttonLength):
            startButton = True
        elif (screen_height / 2) < y < ((screen_height / 2) + buttonLength):
            help = True
        elif ((screen_height / 2) + 100) < y < ((screen_height / 2) + 100 + buttonLength):
            credits = True

    # Menu Text
    textSurface = fontMenu.render("Physics Simulator", True, LIGHTGRAY)
    w, h = fontMenu.size("Physics Simulator")
    screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) - 200))

    # Start Button
    startText = "Start!"
    if startButton:
        pygame.draw.rect(screen, WHITE, (screen_width / 2 - (buttonWidth / 2), (screen_height / 2) - 100, buttonWidth, buttonLength), 0, 10)
        textSurface = fontMenu.render(startText, True, BLACK)
        w, h = fontMenu.size(startText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) - 100))
    else:
        pygame.draw.rect(screen, LIGHTGRAY, (screen_width / 2 - (buttonWidth / 2), (screen_height / 2) - 100, buttonWidth, buttonLength), 2, 10)
        textSurface = fontMenu.render(startText, True, LIGHTGRAY)
        w, h = fontMenu.size(startText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) - 100))

    # Help Button
    helpText = "Help"
    if help:
        pygame.draw.rect(screen, WHITE, (screen_width / 2 - (buttonWidth / 2), (screen_height / 2), buttonWidth, buttonLength), 0, 10)
        textSurface = fontMenu.render(helpText, True, BLACK)
        w, h = fontMenu.size(helpText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2)))
    else:
        pygame.draw.rect(screen, LIGHTGRAY, (screen_width / 2 - (buttonWidth / 2), (screen_height / 2), buttonWidth, buttonLength), 2, 10)
        textSurface = fontMenu.render(helpText, True, LIGHTGRAY)
        w, h = fontMenu.size(helpText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2)))

    # Credits Button
    creditText = "Credits"
    if credits:
        pygame.draw.rect(screen, WHITE, (screen_width / 2 - (buttonWidth / 2), (screen_height / 2) + 100, buttonWidth, buttonLength), 0, 10)
        textSurface = fontMenu.render(creditText, True, BLACK)
        w, h = fontMenu.size(creditText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) + 100))
    else:
        pygame.draw.rect(screen, LIGHTGRAY, (screen_width / 2 - (buttonWidth / 2), (screen_height / 2) + 100, buttonWidth, buttonLength), 2, 10)
        textSurface = fontMenu.render(creditText, True, LIGHTGRAY)
        w, h = fontMenu.size(creditText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2)  + 100))

# Draws the secondary set of buttons
def drawSecondMenu():
    buttonWidth = 300
    buttonLength = 80
    pos = pygame.mouse.get_pos()
    x, y = pos[0], pos[1]
    screen_width, screen_height = pygame.display.get_surface().get_size()
    solarSim = False
    gravSim = False

    # Checks where the mouse is and enables the corresponding buttons
    if (screen_width / 2 - (buttonWidth / 2)) < x < (screen_width / 2 - (buttonWidth / 2) + buttonWidth):
        if ((screen_height / 2) - 100) < y < ((screen_height / 2) - 100 + buttonLength):
            solarSim = True
        elif (screen_height / 2) < y < ((screen_height / 2) + buttonLength):
            gravSim = True


    # Menu Text
    textSurface = fontMenu.render("Physics Simulator", True, LIGHTGRAY)
    w, h = fontMenu.size("Physics Simulator")
    screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) - 200))

    # Solar System Button
    solarSimText = "Solar System"
    if solarSim:
        pygame.draw.rect(screen, WHITE,
                         (screen_width / 2 - (buttonWidth / 2), (screen_height / 2) - 100, buttonWidth, buttonLength),
                         0, 10)
        textSurface = font.render(solarSimText, True, BLACK)
        w, h = font.size(solarSimText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) - 100 + (h/3)))
    else:
        pygame.draw.rect(screen, LIGHTGRAY,
                         (screen_width / 2 - (buttonWidth / 2), (screen_height / 2) - 100, buttonWidth, buttonLength),
                         2, 10)
        textSurface = font.render(solarSimText, True, LIGHTGRAY)
        w, h = font.size(solarSimText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) - 100 + (h/3)))

    # Gravity Simulator
    gravSimText = "Gravity Simulator!"
    if gravSim:
        pygame.draw.rect(screen, WHITE,
                         (screen_width / 2 - (buttonWidth / 2), (screen_height / 2), buttonWidth, buttonLength),
                         0, 10)
        textSurface = font.render(gravSimText, True, BLACK)
        w, h = font.size(gravSimText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) + (h/3)))
    else:
        pygame.draw.rect(screen, LIGHTGRAY,
                         (screen_width / 2 - (buttonWidth / 2), (screen_height / 2), buttonWidth, buttonLength),
                         2, 10)
        textSurface = font.render(gravSimText, True, LIGHTGRAY)
        w, h = font.size(gravSimText)
        screen.blit(textSurface, (screen_width / 2 - (w / 2), (screen_height / 2) + (h/3)))

main()

# pygame.draw.circle(screen, YELLOW, (screenWidth/2, screenHeight/2), 20)
"""pygame.draw.circle(screen, GRAY, (screenWidth / 2 + 60, screenHeight / 2), 4)
            pygame.draw.circle(screen, BROWN, (screenWidth/2 + 100, screenHeight/2), 6)
            pygame.draw.circle(screen, BLUE, (screenWidth / 2 + 140, screenHeight / 2), 8)
            pygame.draw.circle(screen, TERRACOTTA, (screenWidth / 2 + 180, screenHeight / 2), 4)
            pygame.draw.circle(screen, BRASS, (screenWidth / 2 + 220, screenHeight / 2), 14)
            pygame.draw.circle(screen, CAMEL, (screenWidth / 2 + 260, screenHeight / 2), 12)
            pygame.draw.circle(screen, POWDERBLUE, (screenWidth / 2 + 300, screenHeight / 2), 10)
            pygame.draw.circle(screen, ROYALBLUE, (screenWidth / 2 + 340, screenHeight / 2), 10)
            pygame.draw.circle(screen, CYANBLUE, (screenWidth / 2 + 380, screenHeight / 2), 2)"""
