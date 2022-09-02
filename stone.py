import random
import pygame
from pygame import image

BLACK = 0, 0, 0


class Stone:
    STONE_WIDTH = 30
    STONE_HEIGHT = 30
    stone_image = image.load(r"C:\Users\filip\Downloads\stone-pixel-art.png")
    st = pygame.transform.scale(stone_image, (STONE_WIDTH, STONE_HEIGHT))

    def __init__(self, window):
        self.window = window
        self.stonePositionX = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.stonePositionY = -5
        self.stoneRect = self.st.get_rect()

    def stoneFalling(self):
        self.stonePositionY += self.stoneSpeed
        self.stoneRect.y = self.stonePositionY
        self.stoneRect.x = self.stonePositionX

    def drawStone(self):
        pygame.draw.rect(self.window, BLACK, self.stoneRect, 1)
        self.window.blit(self.st, (self.stonePositionX, self.stonePositionY))
        self.stoneFalling()
