import pygame
import random
import math
from pygame import mixer


# Create game window---------------------------------------------------------------------------------------------------
# Intialize the pygame, ALWAYS to make the game run
pygame.init()

# create the screen (by pixel) (x,y)
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

# Background
background = pygame.image.load('background3.png')

# Background Sound
mixer.music.load('Gundam Unicorn- Unicorn Theme.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("No Boi's Sky")
icon = pygame.image.load('spaceship (1).png')
pygame.display.set_icon(icon)

# Player--------------------------------------------------------------------------------------------------------------
playerShip = pygame.image.load('space battleship.png')
# player original location
playerX = 370
playerY = 480
# player location change
playerXchange = 0

# Enemy--------------------------------------------------------------------------------------------------------------
# create empty list to add enemies in the list at the same time
enemyShip = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
enemiesNum = 6

# 'for' loop so 6 enemies can spawn at a same time
for i in range(enemiesNum):

# add first enemy inside the 'enemyShip' list
    # add first enemy inside the 'enemyShip' list
    enemyShip.append(pygame.image.load('robot.png'))
    enemyShip.append(pygame.image.load('alien (1).png'))
    enemyShip.append(pygame.image.load('monsters.png'))
    # enemy original location, spawn randomly
    enemyX.append(random.randint(0,736))# (enemy ship is 64 pixels, 800 - 64 = 736),boundary x-axis
    enemyY.append(random.randint(50,150))# spawn and respawn about 50 to 200 pixels, boundary y-axis
    # enemy location change
    enemyXchange.append(3)
    enemyYchange.append(40)

# Bullet--------------------------------------------------------------------------------------------------------------
bulletImage = pygame.image.load('bullet.png')
# Bullet location
bulletX = 0
bulletY = 480
# Bullet location change
bulletYchange = 10
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"
# Score---------------------------------------------------------------------------------------------------------------
scoreValue = 0
font = pygame.font.FontType('Cyberpunks.ttf',50)
textX = 10
textY = 10
# Game over text------------------------------------------------------------------------------------------------------
overFont = pygame.font.FontType('Cyberpunks.ttf',80)

def showScore(x,y):
    score = font.render("Score : " + str(scoreValue), True, (255,255,255))# put score on the screen
    screen.blit(score, (x,y))

def gameoverShow():
    overText = overFont.render('GAME OVER', True, (255,255,255))
    screen.blit(overText, (200,250))

def player(x,y):
    screen.blit(playerShip,(x,y))# put player on the screen


def enemy(x,y,i):
    screen.blit(enemyShip[i], (x,y))# put enemy on the screen

def fireBullet(x,y):
    global bullet_state # global, so when press 'space', bullet_state change from "ready" to "fire"
    bullet_state = "fire"
    screen.blit(bulletImage,(x + 16, y + 10))# the bullet will locate in the middle top of space ship

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Formula of collision distance between 2 points and midpoint
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True # Collision had occur
    else:
        return False

# Game Loop, make the window stay without close down, until click QUIT----------------------------------------------
running = True
while running:

    # This have to be above all other features of game
    # So the "color screen" this not cover other features
    # RGB - Red, Green, Blue, create color screen
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background,(0,0))

    # go through all the events happened in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # create QUIT button, so the system do not hang
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN: # Keys button that pressed
            # If pressed left key, player moves 0.5 pixels to the left
            if event.key == pygame.K_LEFT:
                playerXchange = -5
            # if pressed right key, player moves 0.5 pixels to the right
            if event.key == pygame.K_RIGHT:
                playerXchange = 5
            # if pressed space, player shoots bullets
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready": #only "fire" again when the bullet_state reset to "ready"
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX # bullet will start at the same location as player
                    fireBullet(bulletX,bulletY)

        if event.type == pygame.KEYUP: # Keys button that release
            # if release any keys, player stops moving (pixel = 0)
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0

    # add movements to the game event-------------------------------------------------------------------------------
    # which is playerX (original location) add with playerXchange (player location change)
    playerX += playerXchange

    # the limit boundary of the ship left movement
    if playerX <= 0:
        playerX = 0
    # the limit boundary of the ship right movement
    # the battleship is 64 pixels, the screen is 800 pixels, 800-64 = 736 pixels
    elif playerX >= 736:
        playerX = 736

    # add enemy movement to the game event---------------------------------------------------------------------
    for i in range(enemiesNum):

        # Game Over
        if enemyY[i] > 400 :
            for j in range(enemiesNum):
                enemyY[j] = 2000
            gameoverShow() # Game Over text pops up
            break


        # which is enemyX (original location) add with enemyXchange (enemy location change)
        enemyX[i] += enemyXchange[i]
        # When enemy hits the left boundary, it will change direction to the right
        if enemyX[i] <= 0:
            enemyXchange[i] = 3
            enemyY[i] += enemyYchange[i]
        # When enemy hits the right boundary, it will change direction to the left
        elif enemyX[i] >= 736:
            enemyXchange[i] = -3
            enemyY[i] += enemyYchange[i]

        # Bullet and Enemy Collision
        # inside 'for' loops, so it will count ALL enemies collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            scoreValue += 1
            # enemy will respawn at random location
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Enemy ship appear on the screen with x,y position
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fireBullet(bulletX,bulletY)
        bulletY -= bulletYchange # bullet go upward when "fire"
    # reset the bullet when it reachs the top of the screen, so the space ship can shoot multiple times
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"


    # Update Battleship appear on the screen with x,y position
    player(playerX, playerY)
    # Update score appear on the screen
    showScore(textX,textY)

    # Update features, ALWAYS after update or add more feature to game-------------------------------------------------
    pygame.display.update()
    clock.tick(300)




