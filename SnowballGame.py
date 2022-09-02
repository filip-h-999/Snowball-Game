import pygame
from pygame import image, font
from player import Player
from stone import Stone
from snowBall import SnowBall
from direction import Direction

gameStarted = False
gameOver = False
score = 0


def main():
    WINDOW_WIDTH = 742
    WINDOW_HEIGHT = 428
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    BLACK = 0, 0, 0
    # RED = 255, 0, 0

    start_screen = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\startscreen.png"), (742, 468))
    game_over_screen = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\gameOver.png"), (742, 468))
    back = pygame.transform.scale(image.load(r"C:\Users\filip\Downloads\back2.png"), (742, 468))

    running = True

    speed = 60
    clock = pygame.time.Clock()

    timerSpeed = 650
    FALL = pygame.USEREVENT + 1
    FALLING_EVENT = pygame.event.Event(FALL)
    direction = Direction.none
    stones = []
    snowB = []
    pygame.init()
    pygame.display.set_caption("Snowball Game")
    player = Player(window)

    def enemyStone():
        for kamen in stones:
            kamen.drawStone()
            if kamen.stonePositionY > 310:
                stones.remove(kamen)

    def snowballs():
        for snow in snowB:
            snow.drawSnowBall()
            if snow.snowballPositionY > 310:
                snowB.remove(snow)
            if player.collisionRect.colliderect(snow.snowBallRect):
                player.inflate(5)
                snowB.remove(snow)

    def dead():
        global gameOver
        for kamen in stones:
            if player.collisionRect.colliderect(kamen.stoneRect):
                gameOver = True
                stones.clear()
                snowB.clear()
                break

    def scoreCounter():
        font1 = font.SysFont('didot.ttc', 35)
        gameScore = font1.render("Score: %d" % score, True, BLACK)
        window.blit(gameScore, (10, 10))

    def restart():
        global gameOver, gameStarted, score
        gameOver = False
        gameStarted = True
        score = 0
        pygame.time.set_timer(FALLING_EVENT, 1000, 1)
        return Player(window)

    while running:
        global gameOver, gameStarted, score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event == FALLING_EVENT and gameStarted and not gameOver:
                stones.append(Stone(window))
                snowB.append(SnowBall(window))
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
            enemyStone()
            dead()
            snowballs()
            player.moveBall(direction)

        if gameOver:
            window.blit(game_over_screen, (0, 0))
            font2 = font.SysFont('didot.ttc', 45)
            gameScore2 = font2.render("Score: %d" % score, True, BLACK)
            window.blit(gameScore2, (310, 332))

        if player.isDead():
            gameOver = True

        pygame.display.update()
        clock.tick(speed)


main()
