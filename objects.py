import pygame

# Initializing Pygame
pygame.init()

"""-------------------------------"""
#            OBJECTIVES
"""-------------------------------"""

# The rockets actively seek the Objective.
class Objective:
    def __init__(self, surface, screenSize):
        # This will always be drawn in the center of the screen.
        # 20 is (somewhat) the radius of the circle
        self.posX = screenSize[0] / 2 - 20
        self.posY = screenSize[1] / 2 - 20
        self.surface = surface
        self.image = pygame.image.load("Rocket_Circle.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

    # Draws the objective onto the screen.
    def drawObjective(self):
        self.surface.blit(self.image, (self.posX, self.posY))


"""-------------------------------"""
#             OBSTACLES
"""-------------------------------"""

# This is what the rockets need to "maneuver" around to get to the objective.
class Obstacles:
    def __init__(self, surface, posValues):
        self.posX = posValues[0]
        self.posY = posValues[1]
        self.surface = surface
        self.image = pygame.image.load(posValues[2]).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        # This is used for checks to see if there is an open path from the rocket to the obj.
        self.rect = pygame.Rect(self.posX, self.posY, self.image.get_size()[0], self.image.get_size()[1])

    # Draws the obstacle onto the screen.
    def drawObstacle(self):
        self.surface.blit(self.image, (self.posX, self.posY))


"""-------------------------------"""
#              ROCKETS
"""-------------------------------"""

# Code for the Rockets Class. This is where the bulk of the calculations lie.
class Rockets:
    def __init__(self, surface, posX, posY, debug = False):
        self.posX = posX
        self.posY = posY
        self.velX = .15
        self.velY = -.15
        self.surface = surface
        self.debug = debug
        self.image = pygame.image.load("Rocket_Arrow.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        # This is used to check if the Rocket has hit the objective.
        # If so, then the rocket will stop moving.
        self.objectiveHit = False

        # This prevents glitches with the rockets getting stuck while heading to the objective.
        self.objectiveLocked = False

    # Draws the rocket and calculates the Rocket's angle.
    def drawRocket(self, objectiveCords = None):
        # Since the rocket only moves diagonally, there is no reason to
        angle = 0
        # Python's degrees start at where a normal degree circle = pi/2, not 2pi. Weird.
        if self.velX > 0:
            if self.velY > 0:
                angle = 225
            else:
                angle = 315
        elif self.velX < 0:
            if self.velY > 0:
                angle = 135
            else:
                angle = 45

        # Rotates the image according to where it is headed.
        # I need to reset the image before changing it for angle changes to be accurate.
        self.image = pygame.image.load("Rocket_Arrow.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)

        # Draws the image onto the screen
        self.surface.blit(self.image, (self.posX, self.posY))

        if self.objectiveHit == False and self.debug == True:
            # This line demonstrates what is between the Rocket and the Objective.
            # If there is nothing in between (checked using clearPath()), then it goes to the objective.
            # Its mostly there for debug.
            pygame.draw.line(self.surface, "Green", objectiveCords, (self.posX, self.posY), 5)

    # Changes Rocket Position
    def wander(self):
        # Final position change
        self.posX += self.velX
        self.posY += self.velY

    """-------------------------------"""
    #         ROCKET COLLISIONS
    """-------------------------------"""

    # Collisions with the Screen
    def screenCollision(self, screenSize):
        screenLeft = 0
        screenRight = screenSize[0]
        screenUp = 0
        screenDown = screenSize[1]
        if self.posX <= screenLeft or self.posX >= screenRight:
            self.velX *= -1
        if self.posY <= screenUp or self.posY >= screenDown:
            self.velY *= -1

    # Collisions against Walls
    def obstacleCollision(self, obstacle):
        # Utilizes Masks with the Rockets for accurate collision.
        # https://www.pygame.org/docs/ref/mask.html
        for i in obstacle:
            offSet = (int(i.posX - self.posX), int(i.posY - self.posY))
            if type(self.mask.overlap(i.mask, offSet)) == tuple:

                # These are the sizes of the objects in (width, height)
                obstacleSize = i.mask.get_size()
                rocketSize = self.mask.get_size()

                if self.posX < i.posX or (obstacleSize[0] + i.posX) < (rocketSize[0] + self.posX):
                    self.velX *= -1

                if self.posY < i.posY or (obstacleSize[1] + i.posY) < (rocketSize[1] + self.posY):
                    self.velY *= -1

    # Collisions against the Objective
    def objectiveCollision(self, objective):
        # Collision with the objective
        offSet = (int(objective.posX - self.posX), int(objective.posY - self.posY))
        # Once the rocket hits the objective, it stops moving.
        if type(self.mask.overlap(objective.mask, offSet)) == tuple:
            self.velY = 0
            self.velX = 0
            # It will also cancel the main loop and only draw the rocket.
            self.objectiveHit = True

    # If there is a clear path from the rocket to the circle, take the path.
    def clearPath(self, obstacles, objective):
        clear = True
        for i in obstacles:
            blocked = i.rect.clipline((self.posX, self.posY), (objective.posX, objective.posY))
            if len(blocked) >= 1:
                clear = False
        if clear:
            dy = (objective.posY - self.posY)
            dx = (objective.posX - self.posX)
            # Makes the Rocket home in on the Objective
            self.velY = dy
            self.velX = dx
            self.velY /= 1000
            self.velX /= 1000
            self.objectiveLocked = True

    """-------------------------------"""
    #           ROCKET LOOP
    """-------------------------------"""

    # The main loop for Rocket Calculations.
    # Its an easy way to manage which functions are called.
    def mainLoop(self, SCREENDIMENSIONS, obstacles, circle):
        if self.objectiveHit:
            """   LOOP IF OBJECTIVE IS HIT   """
            self.drawRocket()

        elif self.objectiveLocked:
            """   LOOP IF PATH TO OBJECTIVE IS CLEAR   """
            # Collisions
            self.screenCollision(SCREENDIMENSIONS)
            self.objectiveCollision(circle)

            # Change in Rocket Position
            self.wander()

            # Drawing the Rocket
            self.drawRocket((circle.posX, circle.posY))

        else:
            """   MAIN LOOP   """
            # Collisions
            self.screenCollision(SCREENDIMENSIONS)
            self.obstacleCollision(obstacles)
            self.objectiveCollision(circle)

            # If no obstacles are present from rocket to circle, go to circle.
            self.clearPath(obstacles, circle)

            # Change in Rocket Position
            self.wander()

            # Drawing the Rocket
            self.drawRocket((circle.posX, circle.posY))
