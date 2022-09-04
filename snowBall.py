import random
import pygame
from pygame import image

BLACK = 0, 0, 0


class SnowBall:
    SNOWBALL_WIDTH = 20
    SNOWBALL_HEIGHT = 20
    snowball_image = image.load(r"assets\images\snowball.png")
    sn1 = pygame.transform.scale(snowball_image, (SNOWBALL_WIDTH, SNOWBALL_HEIGHT))
    sn2 = pygame.transform.scale(snowball_image, (25, 25))
    sn3 = pygame.transform.scale(snowball_image, (33, 33))

    def __init__(self, window):
        self.window = window
        self.snSize = random.randrange(1, 3, 1)
        self.randomSn = [self.sn1, self.sn2, self.sn3][self.snSize]
        self.snowballPositionX = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.snowballPositionY = -5
        self.snowBallRect = self.randomSn.get_rect()

    def snowFalling(self):
        self.snowballPositionY += self.stoneSpeed
        self.snowBallRect.y = self.snowballPositionY
        self.snowBallRect.x = self.snowballPositionX

    def drawSnowBall(self):
        self.window.blit(self.randomSn, (self.snowballPositionX, self.snowballPositionY))
        self.snowFalling()
        # pygame.draw.rect(self.window, BLACK, self.snowBallRect, 1)
