import pygame
from star_data import star
import random
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (175, 201, 255)
LIGHTORANGE = (255, 217, 178)
STARCOLORS = [WHITE, LIGHTORANGE, LIGHTBLUE]

screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()

def main():
    starList = createStars()
    mainLoop = True
    mainSimulation = True

    # Main loop that handles all the screens
    while mainLoop:

        # This loop handles the simulation screen
        while mainSimulation:
            clock.tick(2)
            screen.fill(BLACK)

            # Events like key presses and mouse movements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                    mainSimulation = False


            drawStars(starList)
            pygame.display.update()


# Initializes the array of star objects
def createStars():
    # Creates an array of 100 elements
    starList = [0] * 100
    chanceOfMovingStars = 5
    chanceOfFlickering = 5
    screenWidth, screenHeight = pygame.display.get_surface().get_size()
    for x in range(len(starList)):
        # Some parameters for the stars
        posX = random.randint(0, screenWidth)
        posY = random.randint(0, screenHeight)
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


main()
