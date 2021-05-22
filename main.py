import pygame
import objects as obj

# Initializing Pygame
pygame.init()

# Setting up Screen Dimensions
SCREENDIMENSIONS = (600, 400)
screen = pygame.display.set_mode((SCREENDIMENSIONS[0], SCREENDIMENSIONS[1]))
pygame.display.set_caption("Homing Rockets")

# Setting up Background
background = pygame.Surface(SCREENDIMENSIONS)
background.fill((200, 200, 200))

"""-------------------------------"""
#            PRE-START
"""-------------------------------"""

# This while loop ensures the program gets the necessary number of obstacles & rockets that the user wants.
while True:
    rocketNumber = input("Please input the number of rockets you would like.\n>>> ")
    obstacleNumber = input("Please input the number of obstacles you would like.\n>>> ")
    try:
        rocketNumber = int(rocketNumber)
        obstacleNumber = int(obstacleNumber)

        # This ensures too many rockets or obstacles aren't on the screen at once.
        if rocketNumber > 5:
            print("Number of Rockets too large, defaulting to 3.")
            rocketNumber = 4
        elif rocketNumber <= 0:
            print("Number of Rockets too small, defaulting to 1.")
            rocketNumber = 1

        # Ensures there are enough obstacles and rockets for the program to run.
        if obstacleNumber > 4:
            print("Number of Obstacles too large, defaulting to 4.")
            obstacleNumber = 4
        elif obstacleNumber <= 0:
            print("Number of Obstacles too small, defaulting to 1.")
            obstacleNumber = 1

        # A check to see if debug lines should be on.
        debug = input("Enable Debug Mode? [Y/N]\n>>> ").lower()
        if debug == "y":
            debug = True
        else:
            debug = False
        break
    except:
        print("Your input needs to be an integer")

"""-------------------------------"""
#       INITIALIZING OBJECTS
"""-------------------------------"""
# Initializing the Objective & its location.
circle = obj.Objective(background, SCREENDIMENSIONS)

# Initializing the Obstacles & their location
## Found this trick on stack Overflow, really helps with automating making objects.
obstaclePositions = [(200, 90, "Obstacle1.png"), (400, 90, "Obstacle2.png"),
                     (250, 280, "Obstacle3.png"), (90, 85, "Obstacle4.png")]
obstacles = [obj.Obstacles(background, obstaclePositions[x]) for x in range(0, obstacleNumber)]

# Initializing Rockets
rocketPositions = [(500, 50), (500, 220), (20, 20), (40, 60)]
rockets = [obj.Rockets(background, rocketPositions[x-1][0], rocketPositions[x-1][1], debug) for x in range(0, rocketNumber)]

# Found this while looking for ways to optimize the program. It came from here:
# https://codeproject.com/Articles/5298051/Improving-Performance-in-Pygame-Speed-Up-Your-Game
# Less checks equate to a faster runtime.
pygame.event.set_allowed([pygame.QUIT])

"""-------------------------------"""
#             CORE LOOP
"""-------------------------------"""

# Core Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Making Background
    background.fill((200, 200, 200))

    # Drawing background onto the screen
    screen.blit(background, (0, 0))

    ## Initializing and updating screen.
    # Drawing Objective
    circle.drawObjective()

    # Drawing obstacles
    for i in obstacles:
        i.drawObstacle()

    # Calculations for rockets.
    for i in rockets:
        i.mainLoop(SCREENDIMENSIONS, obstacles, circle)

    # Drawing background onto the screen
    screen.blit(background, (0, 0))

    pygame.display.flip()
