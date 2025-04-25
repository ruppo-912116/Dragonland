import pygame
from pygame.locals import *
import time
import random

# Initialize Pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('DragonLand')
FPS = 40

# Set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Load assets
playerImg = pygame.image.load('shooter.png')
playerRect = playerImg.get_rect()
enemyImg = pygame.image.load('dragon.png')
enemyRect = enemyImg.get_rect()
background = pygame.image.load('background.jpg')
background1 = pygame.transform.scale(background, (800, 600))
arrowImg = pygame.image.load('arrow.png')
arrowRect = arrowImg.get_rect()

# Variables
moveSpeed = 5
enemycount = 40
enemy = []
arrows = []
coll = False

font = pygame.font.SysFont(None, 48)
font1 = pygame.font.SysFont(None, 24)


def surfaceo(surface):
    surface.blit(background1, (0, 0))


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    pygame.display.update()
    time.sleep(2)


def collisiontest(p, b):
    return p.colliderect(b['rect'])


def waitforkeypress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_RETURN or event.key == K_c:
                    return


def scoredisplay(score):
    text = font1.render("Score: " + str(score), True, BLACK)
    windowSurface.blit(text, (0, 0))


def lives(life):
    text = font1.render("Lives: " + str(life), True, BLACK)
    windowSurface.blit(text, (0, 15))


# Initial enemy setup
x = 0
for i in range(8):
    newEnemy = {'rect': pygame.Rect(720, x, 80, 60), 'speed': random.randint(1, 8)}
    enemy.append(newEnemy)
    x += 70

# Main game variables
score = 0
addnewenemy = 0
life = 1
flag = 0
start = True
gameLoop = True
i = 0
move = False
bull = []
keyspace = True

while gameLoop:
    while start:
        surfaceo(windowSurface)
        drawText('A simple 2D game', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 40)
        drawText('Rupan Inc.', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 70)
        drawText('Press ENTER..', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 200)
        waitforkeypress()
        start = False

    # Fill the canvas with a white background
    windowSurface.fill(WHITE)

    # Detect key presses
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == K_SPACE:
                move = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

    # Player movement restrictions
    if keys[pygame.K_UP] and playerRect.top > 0:
        playerRect.top -= moveSpeed
    if keys[pygame.K_DOWN] and playerRect.bottom < WINDOWHEIGHT:
        playerRect.top += moveSpeed
    if keys[pygame.K_SPACE] and keyspace:
        x = playerRect.right - 15
        y = (playerRect.top + playerRect.bottom) / 2 - 10
        move = True
        i = 0
        keyspace = False
        newEnemy = {'rect': pygame.Rect(x, y, 20, 20), 'speed': 5}
        bull.append(newEnemy)

    i += 1
    if i > 10:
        keyspace = True
        i = 0

    # Draw player
    windowSurface.blit(playerImg, playerRect)

    # Add new enemies
    if addnewenemy == enemycount:
        addnewenemy = 0
        newEnemy = {'rect': pygame.Rect(720, random.randint(0, 540), 80, 60), 'speed': random.randint(1, 4)}
        enemy.append(newEnemy)

    # Remove enemies reaching the left end
    for b in enemy[:]:
        if b['rect'].left < -2:
            flag += 1
            enemy.remove(b)

    # Player and enemy collision
    for b in enemy[:]:
        if collisiontest(playerRect, b):
            life -= 1
            enemy.remove(b)

    # Bullet and enemy collision
    for bulls in bull[:]:
        for enemys in enemy[:]:
            if collisiontest(bulls['rect'], enemys):
                score += 1
                enemy.remove(enemys)
                bull.remove(bulls)
                break
        if bulls['rect'].right > 700:
            bull.remove(bulls)

    if flag == 3:
        life -= 1
        flag = 0

    scoredisplay(score)
    lives(life)

    # Game-over screen
    if life == 0:
        windowSurface.fill(WHITE)
        text = font.render("GAME OVER!!!", True, BLACK)
        text1 = font.render("Press C to continue and ESC to exit the game", True, BLACK)
        windowSurface.blit(text, (300, 200))
        windowSurface.blit(text1, (100, 300))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == K_c:
                        # Reset variables
                        life = 1
                        score = 0
                        enemy = []
                        bull = []
                        flag = 0
                        x = 0
                        for i in range(8):
                            newEnemy = {'rect': pygame.Rect(720, x, 80, 60), 'speed': random.randint(1, 8)}
                            enemy.append(newEnemy)
                            x += 70
                        start = True
                        break
            if start:
                break

    # Draw enemies
    for b in enemy:
        b['rect'].move_ip(-b['speed'], 0)
        windowSurface.blit(enemyImg, b['rect'])

    # Draw bullets
    for b in bull:
        b['rect'].move_ip(+b['speed'], 0)
        windowSurface.blit(arrowImg, b['rect'])

    mainClock.tick(FPS)
    addnewenemy += 1
    pygame.display.update()
