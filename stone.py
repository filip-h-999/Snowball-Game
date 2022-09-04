import random
import pygame
from pygame import image

BLACK = 0, 0, 0


class Stone:
    STONE_WIDTH = 30
    STONE_HEIGHT = 30
    stone_image = image.load(r"assets\images\stone-pixel-art.png")
    st1 = pygame.transform.scale(stone_image, (STONE_WIDTH, STONE_HEIGHT))
    st2 = pygame.transform.scale(stone_image, (25, 25))
    st3 = pygame.transform.scale(stone_image, (33, 33))

    def __init__(self, window):
        self.window = window
        self.stSize = random.randrange(1, 3, 1)
        self.randomSt = [self.st1, self.st2, self.st3][self.stSize]
        self.stonePositionX = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.stonePositionY = -5
        self.stoneRect = self.randomSt.get_rect()

    def stoneFalling(self):
        self.stonePositionY += self.stoneSpeed
        self.stoneRect.y = self.stonePositionY
        self.stoneRect.x = self.stonePositionX

    def drawStone(self):
        self.window.blit(self.randomSt, (self.stonePositionX, self.stonePositionY))
        self.stoneFalling()
        pygame.draw.rect(self.window, BLACK, self.stoneRect, 1)
