import random
from enum import Enum
import pygame
from pygame import image


WINDOW_WIDTH = 742
WINDOW_HEIGHT = 428

BALL_WIDTH = 55
BALL_HEIGHT = 55
BALL_X_POSITION = 355
BALL_Y_POSITION = 295

ball_image = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\snowball.png"), (BALL_WIDTH, BALL_HEIGHT))
back = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\back2.png"), (742, 468))
image_right = pygame.transform.rotate(ball_image, 90)
image_left = pygame.transform.rotate(ball_image, -90)

BLACK = (0, 0, 0)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True

speed = 60
clock = pygame.time.Clock()

pygame.time.set_timer(pygame.USEREVENT, 100)
counter = 1


class Stone:
    STONE_WIDTH = 30
    STONE_HEIGHT = 30
    stone_image = image.load(r"C:\Users\filip\Downloads\stone-pixel-art.png")
    st = pygame.transform.scale(stone_image, (STONE_WIDTH, STONE_HEIGHT))

    def __init__(self):
        self.x = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.y = -5

    def stoneFalling(self):
        self.y += self.stoneSpeed


class Direction(Enum):
    left = 1
    right = 2
    none = 3


direction = Direction.none


def main():
    global running
    stones = []
    pygame.init()
    pygame.display.set_caption("Snowball Game")

    while running:
        global direction, counter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                counter -= 1
                if counter == 0:
                    stones.append(Stone())
                    counter = 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = Direction.left
                if event.key == pygame.K_RIGHT:
                    direction = Direction.right
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    direction = Direction.none

        window.blit(back, (0, 0))
        ball()
        stones2(stones)
        moveBall(direction)
        pygame.display.update()
        clock.tick(speed)


def ball():
    window.blit(ball_image, (BALL_X_POSITION, BALL_Y_POSITION))


def moveBall(dire):
    global BALL_Y_POSITION, BALL_X_POSITION
    if dire == Direction.left:
        BALL_X_POSITION -= 3
    elif dire == Direction.right:
        BALL_X_POSITION += 3


def stones2(stones: list[Stone]):
    for kamen in stones:
        window.blit(kamen.st, (kamen.x, kamen.y))
        kamen.stoneFalling()
        if kamen.y > 310:
            stones.remove(kamen)


main()
