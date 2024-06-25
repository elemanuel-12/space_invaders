import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

mixer.music.load('background_music.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(2)
    alienY_change.append(40)

# laser
# ready - can't see laser on the screen
# fire - laser is currenlty moving

laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0 ,255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(alienX, alienY, laserX, laserY):
    distance = math.sqrt(math.pow(alienX - laserX, 2) + (math.pow(alienY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    laser_Sound = mixer.Sound('laser.wav')
                    laser_Sound.play()
                    laserX = playerX
                    fire_laser(playerX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # bounds

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # alien movement
    for i in range(num_of_aliens):

        #game over
        if alienY[i] >440:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
             alienX_change[i] = -3
             alienY[i] += alienY_change[i]

        # collision
        collision = isCollision(alienX[i], alienY[i], laserX, laserY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    # laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
