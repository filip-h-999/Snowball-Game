import random
from enum import Enum
import pygame
from pygame import image, font

WINDOW_WIDTH = 742
WINDOW_HEIGHT = 428
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = 0, 0, 0
RED = 255, 0, 0

start_screen = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\startscreen.png"), (742, 468))
game_over_screen = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\gameOver.png"), (742, 468))

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


class Player:
    def __init__(self):
        self.BALL_WIDTH = 55
        self.BALL_HEIGHT = 55
        self.ball_image = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\snowball.png"),
                                                 (self.BALL_WIDTH, self.BALL_HEIGHT))
        self.ball_image_origin = self.ball_image
        self.rect = self.ball_image.get_rect()
        self.rect.x = 355
        self.rect.y = 295
        self.collisionRect = self.rect.inflate(-15, -15)

    def drawPlayer(self):
        window.blit(self.ball_image, self.rect)
        # pygame.draw.rect(window, BLACK, self.rect, 2)
        pygame.draw.rect(window, RED, self.collisionRect, 2)

    def moveBall(self, dire):
        if dire == Direction.left:
            self.rect.x -= PLAYER_SPEED
        elif dire == Direction.right:
            self.rect.x += PLAYER_SPEED
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
        borderLeft = pygame.draw.rect(window, BLACK, pygame.Rect(-59, 0, 60, 600))
        borderRight = pygame.draw.rect(window, BLACK, pygame.Rect(741, 0, 60, 600))
        if self.rect.colliderect(borderLeft):
            self.rect.x = 685
        if self.rect.colliderect(borderRight):
            self.rect.x = 5

    def isDead(self):
        return self.BALL_WIDTH == 23


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
    player = Player()

    while running:
        global direction, timerSpeed, gameStarted, gameOver, score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event == FALLING_EVENT and gameStarted and not gameOver:
                stones.append(Stone())
                snowB.append(SnowBall())
                timerSpeed -= 1
                player.inflate(-2)
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
                    player = restart()

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
            player.teleportBorder()
            scoreCounter()
            player.drawPlayer()
            enemyStone(stones)
            dead(snowB, stones, player)
            snowballs(snowB, player)
            player.moveBall(direction)

        if gameOver:
            window.blit(game_over_screen, (0, 0))
            font1 = font.SysFont('didot.ttc', 45)
            gameScore = font1.render("Score: %d" % score, True, BLACK)
            window.blit(gameScore, (310, 332))

        if player.isDead():
            gameOver = True

        pygame.display.update()
        clock.tick(speed)


def enemyStone(stones: list[Stone]):
    for kamen in stones:
        # draw kamen funktia
        pygame.draw.rect(window, BLACK, kamen.stoneRect, 1)
        window.blit(kamen.st, (kamen.stonePositionX, kamen.stonePositionY))
        kamen.stoneFalling()
        if kamen.stonePositionY > 310:
            stones.remove(kamen)


def snowballs(snowB: list[SnowBall], pl: Player):
    for snow in snowB:
        pygame.draw.rect(window, BLACK, snow.snowBallRect, 1)
        window.blit(snow.sn, (snow.snowballPositionX, snow.snowballPositionY))
        snow.snowFalling()
        if snow.snowballPositionY > 310:
            snowB.remove(snow)
        if pl.collisionRect.colliderect(snow.snowBallRect):
            pl.inflate(5)
            snowB.remove(snow)


def dead(snowB: list[SnowBall], stones: list[Stone], pl: Player):
    global gameOver
    # pygame.draw.rect(window, BLACK, playerRect, 5)
    for kamen in stones:
        # pygame.draw.rect(window, BLACK, kamen.stoneRect, 1)
        if pl.collisionRect.colliderect(kamen.stoneRect):
            gameOver = True
            stones.clear()
            snowB.clear()
            break


def scoreCounter():
    global score
    font1 = font.SysFont('didot.ttc', 35)
    gameScore = font1.render("Score: %d" % score, True, BLACK)
    window.blit(gameScore, (10, 10))


def restart():
    global gameOver, gameStarted, score
    gameOver = False
    gameStarted = True
    score = 0
    pygame.time.set_timer(FALLING_EVENT, 1000, 1)
    return Player()


main()
