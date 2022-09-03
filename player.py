import pygame
from pygame import image
from direction import Direction


class Player:
    BLACK = 0, 0, 0
    RED = 255, 0, 0

    def __init__(self, window):
        self.window = window
        self.BALL_WIDTH = 55
        self.BALL_HEIGHT = 55
        self.ball_image = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\snowball.png"),
                                                 (self.BALL_WIDTH, self.BALL_HEIGHT))
        self.PLAYER_SPEED = 5.5
        self.ball_image_origin = self.ball_image
        self.rect = self.ball_image.get_rect()
        self.rect.x = 355
        self.rect.y = 295
        self.collisionRect = self.rect.inflate(-15, -15)

    def drawPlayer(self):
        self.window.blit(self.ball_image, self.rect)
        # pygame.draw.rect(window, BLACK, self.rect, 2)
        # pygame.draw.rect(self.window, self.RED, self.collisionRect, 2)

    def moveBall(self, dire):
        if dire == Direction.left:
            self.rect.x -= self.PLAYER_SPEED
        elif dire == Direction.right:
            self.rect.x += self.PLAYER_SPEED
        self.collisionRect = self.rect.inflate(-15, -15)

    def inflate(self, size):
        self.BALL_WIDTH += size
        self.BALL_HEIGHT += size
        self.rect.y -= size/2
        self.rect.x += size/2
        self.ball_image = pygame.transform.scale(self.ball_image_origin, (self.BALL_WIDTH, self.BALL_HEIGHT))
        self.rect.inflate_ip(size, size)
        self.collisionRect = self.rect.inflate(-15, -15)

    def teleportBorder(self):
        borderLeft = pygame.draw.rect(self.window, self.BLACK, pygame.Rect(-59, 0, 60, 600))
        borderRight = pygame.draw.rect(self.window, self.BLACK, pygame.Rect(741, 0, 60, 600))
        if self.rect.colliderect(borderLeft):
            self.rect.x = 685
        if self.rect.colliderect(borderRight):
            self.rect.x = 5

    def isDead(self):
        return self.BALL_WIDTH == 23
