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
PLAYER_SPEED = 5.5

BLACK = (0, 0, 0)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True

speed = 60
clock = pygame.time.Clock()

timerSpeed = 650
FALL = pygame.USEREVENT + 1
FALLING_EVENT = pygame.event.Event(FALL)
pygame.time.set_timer(FALLING_EVENT, 1000, 1)


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


class SnowBall:
    SNOWBALL_WIDTH = 20
    SNOWBALL_HEIGHT = 20
    snowball_image = image.load(r"C:\Users\filip\Downloads\snowball.png")
    sn = pygame.transform.scale(snowball_image, (SNOWBALL_WIDTH, SNOWBALL_HEIGHT))

    def __init__(self):
        self.x = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.y = -5

    def snowFalling(self):
        self.y += self.stoneSpeed


class Direction(Enum):
    left = 1
    right = 2
    none = 3


direction = Direction.none


def main():
    global running
    stones = []
    snowB = []
    pygame.init()
    pygame.display.set_caption("Snowball Game")

    while running:
        global direction, timerSpeed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event == FALLING_EVENT:
                stones.append(Stone())
                snowB.append(SnowBall())
                timerSpeed -= 1
                pygame.time.set_timer(FALLING_EVENT, timerSpeed, 1)
                if timerSpeed < 100:
                    timerSpeed = 100

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = Direction.left
                if event.key == pygame.K_RIGHT:
                    direction = Direction.right
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    direction = Direction.none

        window.blit(back, (0, 0))
        player()
        enemyStone(stones)
        snowballs(snowB)
        moveBall(direction)
        pygame.display.update()
        clock.tick(speed)


def player():
    window.blit(ball_image, (BALL_X_POSITION, BALL_Y_POSITION))


def moveBall(dire):
    global BALL_Y_POSITION, BALL_X_POSITION
    if dire == Direction.left:
        BALL_X_POSITION -= PLAYER_SPEED
    elif dire == Direction.right:
        BALL_X_POSITION += PLAYER_SPEED


def enemyStone(stones: list[Stone]):
    for kamen in stones:
        window.blit(kamen.st, (kamen.x, kamen.y))
        kamen.stoneFalling()
        if kamen.y > 310:
            stones.remove(kamen)


def snowballs(snowB: list[SnowBall]):
    for snow in snowB:
        window.blit(snow.sn, (snow.x, snow.y))
        snow.snowFalling()
        if snow.y > 310:
            snowB.remove(snow)


main()
