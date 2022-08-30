import random
from enum import Enum
import pygame
from pygame import image, font

WINDOW_WIDTH = 742
WINDOW_HEIGHT = 428
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = 0, 0, 0

BALL_WIDTH = 55
BALL_HEIGHT = 55
# BALL_X_POSITION = 355
# BALL_Y_POSITION = 295

start_screen = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\startscreen.png"), (742, 468))
game_over_screen = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\gameOver.png"), (742, 468))

ball_image = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\snowball.png"), (BALL_WIDTH, BALL_HEIGHT))
ball_image_origin = ball_image
playerRect = ball_image.get_rect()
playerRect.x = 355
playerRect.y = 295

back = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\back2.png"), (742, 468))
PLAYER_SPEED = 5.5

running = True
gameStarted = False
gameOver = False

score = 0
speed = 60
clock = pygame.time.Clock()

timerSpeed = 650
FALL = pygame.USEREVENT + 1
FALLING_EVENT = pygame.event.Event(FALL)


class Stone:
    STONE_WIDTH = 30
    STONE_HEIGHT = 30
    stone_image = image.load(r"C:\Users\filip\Downloads\stone-pixel-art.png")
    st = pygame.transform.scale(stone_image, (STONE_WIDTH, STONE_HEIGHT))

    def __init__(self):
        self.stonePositionX = random.randrange(0, 690)
        self.stoneSpeed = random.randrange(1, 3)
        self.stonePositionY = -5
        self.stoneRect = self.st.get_rect()

    def stoneFalling(self):
        self.stonePositionY += self.stoneSpeed
        self.stoneRect.y = self.stonePositionY
        self.stoneRect.x = self.stonePositionX


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
        global direction, timerSpeed, gameStarted, gameOver, score, BALL_WIDTH, BALL_HEIGHT, ball_image
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event == FALLING_EVENT and gameStarted and not gameOver:
                stones.append(Stone())
                snowB.append(SnowBall())
                timerSpeed -= 1
                BALL_WIDTH -= 2
                BALL_HEIGHT -= 2
                playerRect.x += 2
                playerRect.y += 2
                ball_image = pygame.transform.scale(ball_image_origin, (BALL_WIDTH, BALL_HEIGHT))
                pygame.time.set_timer(FALLING_EVENT, timerSpeed, 1)
                if timerSpeed < 100:
                    timerSpeed = 100
                score += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.time.set_timer(FALLING_EVENT, 1000, 1)
                    gameStarted = True
                if event.key == pygame.K_n and gameOver:
                    running = False
                if event.key == pygame.K_c and gameOver:
                    restart()

                if event.key == pygame.K_LEFT:
                    direction = Direction.left
                if event.key == pygame.K_RIGHT:
                    direction = Direction.right
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    direction = Direction.none

        if not gameStarted:
            window.blit(start_screen, (0, 0))

        if gameStarted and not gameOver:
            window.blit(back, (0, 0))
            teleportBorder()
            scoreCounter()
            player()
            enemyStone(stones)
            dead(snowB, stones)
            snowballs(snowB)
            moveBall(direction)

        if gameOver:
            window.blit(game_over_screen, (0, 0))
            font1 = font.SysFont('didot.ttc', 45)
            gameScore = font1.render("Score: %d" % score, True, BLACK)
            window.blit(gameScore, (310, 332))

        if BALL_WIDTH == 23:
            gameOver = True

        pygame.display.update()
        clock.tick(speed)


def player():
    # window.blit(ball_image, (BALL_X_POSITION, BALL_Y_POSITION))
    window.blit(ball_image, playerRect)
    pygame.draw.rect(window, BLACK, playerRect, 5)


def moveBall(dire):
    if dire == Direction.left:
        # BALL_X_POSITION -= PLAYER_SPEED
        playerRect.x -= PLAYER_SPEED
    elif dire == Direction.right:
        # BALL_X_POSITION += PLAYER_SPEED
        playerRect.x += PLAYER_SPEED


def enemyStone(stones: list[Stone]):
    for kamen in stones:
        window.blit(kamen.st, (kamen.stonePositionX, kamen.stonePositionY))
        kamen.stoneFalling()
        if kamen.stonePositionY > 310:
            stones.remove(kamen)


def snowballs(snowB: list[SnowBall]):
    global BALL_WIDTH, BALL_HEIGHT, ball_image
    for snow in snowB:
        # pygame.draw.rect(window, BLACK, snow.snowBallRect, 1)
        window.blit(snow.sn, (snow.snowballPositionX, snow.snowballPositionY))
        snow.snowFalling()
        if snow.snowballPositionY > 310:
            snowB.remove(snow)
        if playerRect.colliderect(snow.snowBallRect):
            BALL_WIDTH += 5
            BALL_HEIGHT += 5
            playerRect.y -= 5
            ball_image = pygame.transform.scale(ball_image, (BALL_WIDTH, BALL_HEIGHT))
            snowB.remove(snow)


def dead(snowB: list[SnowBall], stones: list[Stone]):
    global gameOver
    # pygame.draw.rect(window, BLACK, playerRect, 5)
    for kamen in stones:
        # pygame.draw.rect(window, BLACK, kamen.stoneRect, 1)
        if playerRect.colliderect(kamen.stoneRect):
            gameOver = True
            stones.clear()
            snowB.clear()
            break


def scoreCounter():
    global score
    font1 = font.SysFont('didot.ttc', 35)
    gameScore = font1.render("Score: %d" % score, True, BLACK)
    window.blit(gameScore, (10, 10))


def teleportBorder():
    borderLeft = pygame.draw.rect(window, BLACK, pygame.Rect(-59, 0, 60, 600))
    borderRight = pygame.draw.rect(window, BLACK, pygame.Rect(741, 0, 60, 600))
    if playerRect.colliderect(borderLeft):
        playerRect.x = 685
    if playerRect.colliderect(borderRight):
        playerRect.x = 5


def restart():
    global gameOver, gameStarted, score, BALL_WIDTH, BALL_HEIGHT, ball_image
    gameOver = False
    gameStarted = True
    score = 0
    BALL_WIDTH = 55
    BALL_HEIGHT = 55
    playerRect.y = 295
    playerRect.x = 355
    ball_image = pygame.transform.scale(ball_image_origin, (BALL_WIDTH, BALL_HEIGHT))
    pygame.time.set_timer(FALLING_EVENT, 1000, 1)


main()
