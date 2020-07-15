import pygame
import random
import math
from pygame import mixer #mixer is used for sounds

# INITIALIZE PYGAME
pygame.init()

# CREATE THE SCREEN
# This is a tuple. Need to add in two brackets. Will take in 800=width (x), 600=height(y).
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load('spacebackground.png')

#background sound
mixer.music.load('background_music.mp3')
mixer.music.play(-1) # This plays on loop

# TITLE AND ICON
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load('player.png')
playerX = 370  # x axis horizontal
playerY = 480  # y axis vertical
playerX_change = 0

# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8  # This runs for 6 times to create 6 new enemies within the lists above.

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien_enemy.png'))
    enemyX.append(random.randint(0, 765))  # x axis horizontal
    enemyY.append(random.randint(50, 150))  # y axis vertical
    enemyX_change.append(4)
    enemyY_change.append(30)

# LASER
laserImg = pygame.image.load('shootlaser.png')
laserX = 0
laserY = 480  # This is where the laser will start (top of the spaceship)
laserX_change = 4
laserY_change = 10
laser_state = "ready"  # You can't see the laser on the screen

# SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#GAME OVER
over_font = pygame.font.Font('freesansbold.ttf', 64)

# FUNCTIONS
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    text = over_font.render("GAME OVER", True, (255, 255, 255))
    score = font.render("You Scored: " + str(score_value) + " points", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    screen.blit(score, (240, 350))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 21, y + 10))


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:  # if the distance between the enemy and laser is less than 27 pixels
        return True
    else:
        return False


# GAME LOOP
# 1 - close the screen: While True (while game is active) for each event happening, get each one and if the event type is equal to QUIT (X) then end programme



running = True
while running:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # To check if any key stroke pressed is either left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    # Gets the current x coordinate of the spaceship to ensure the bullet is always fired at the same position
                    laserX = playerX  # When the spacekey is pressed, call the fire_laser function
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Ensuring spaceship in maintained within the screen boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement within the screen boundaries from right to left and right, then drops down y axis when reaching the borders
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000 #ensures when the enemy is at 440 on the Y axis that they are moved at 2000 pixels to the bottom on the screen.
            game_over_text() #out of view
            break # breaking out of the main for i in range loop

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
            # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)  # Save either True or False
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            laserY = 480
            laser_state = "ready"  # Resets the laser status to 'ready' and creates a score
            score_value += 1
            enemyX[i] = random.randint(0, 765)  # This then gets creates a new enemy in a new location on screen
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
# Laser movement - if laser_state is 'fire' (when spacebar is pressed) then decrease the pixels by laserY and save
# to lasterY_change

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"  # This resets the laser to 480 again and 'ready' for shooting again

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
