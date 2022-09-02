import random
import pygame
from pygame import image


class SnowBall:
    SNOWBALL_WIDTH = 20
    SNOWBALL_HEIGHT = 20
    snowball_image = image.load(r"C:\Users\filip\Downloads\snowball.png")
    sn = pygame.transform.scale(snowball_image, (SNOWBALL_WIDTH, SNOWBALL_HEIGHT))

    def __init__(self):
        self.snowballPositionX = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.snowballPositionY = -5
        self.snowBallRect = self.sn.get_rect()

    def snowFalling(self):
        self.snowballPositionY += self.stoneSpeed
        self.snowBallRect.y = self.snowballPositionY
        self.snowBallRect.x = self.snowballPositionX
