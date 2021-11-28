import pygame
import random
import math
from pygame import mixer

pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load('background.png')
DEFAULT_IMAGE_SIZE = (800, 600)
background = pygame.transform.scale(background, DEFAULT_IMAGE_SIZE)

#background sound
mixer.music.load('backmusic.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

#myname
font = pygame.font.SysFont('freesansbold.ttf',1)
name = font.render('created by KaveeshaKF',True,(0,0,0))
nameX = 400
nameY = 550

# player
playerImg = pygame.image.load('rocket.png')
DEFAULT_IMAGE_SIZE = (64, 64)
playerImg = pygame.transform.scale(playerImg, DEFAULT_IMAGE_SIZE)
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo11.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# bullet
#ready - you can't see the bullet screen
#fire - will be able to see the bullet

bulletImg = pygame.image.load('bulleti.png')
DEFAULT_IMAGE_SIZE = (20, 20)
bulletImg = pygame.transform.scale(bulletImg, DEFAULT_IMAGE_SIZE)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_name(x,y):
    name_text = font.render('created by KaveeshaKF', True,(128,0,128))
    screen.blit(name_text, (400, 550))


def show_score(x,y):
    score = font.render('Score :' + str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text(x,y):
    over_text = over_font.render('GAME OVER', True,(255,255,255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))
    # with blit we can draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16, y+10))


def isCollision(enemyX, enemyY,bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY-bulletY , 2)))
    if distance < 27:
        return True
    else:
        return False
# Game loop
running = True
while running:

    # RGB - valus 0,0,0(google, hex to rgb color table)
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key stroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -1  # 0.3 speed of the spaceship
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('gunshot.mp3')
                    bullet_sound.play()
                    #get the current x cordinate of the space ship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # checking for bounderies of space ship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736



    # enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200,250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

         # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.mp3')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 500)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i],i)
    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state ='ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)
    show_name(nameX,nameY)

    pygame.display.update()
