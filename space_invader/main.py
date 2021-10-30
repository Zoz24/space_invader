import pygame 
import random
import math
from pygame import mixer

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('images/background3.jpg')
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('images/ufo.png')
pygame.display.set_icon(icon)

# Music
mixer.music.load('sound/background.wav')
mixer.music.play(-1)

# Player
player_img = pygame.image.load('images/player.png')
player_x = 350
player_y = 500
playerx_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy_img.append(pygame.image.load('images/enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(0.5)
    enemyy_change.append(40)

# Bullet
bullet_img = pygame.image.load('images/bullet.png')
bullet_x = 0
bullet_y = 500
bulletx_change = 2
bullety_change = 3
bullet_state = 'ready'

# Score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def player(x,  y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x, y):
    score = score_font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.7
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('sound/laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Player Movement
    player_x += playerx_change
    if player_x <=0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    for i in range(num_enemies):
        if enemy_y[i] > 465:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        
        enemy_x[i] += enemyx_change[i]
        if enemy_x[i] <= 0:
            enemyx_change[i] = 0.4
            enemy_y[i] += enemyy_change[i]
        elif enemy_x[i] >= 736:
            enemyx_change[i] = -0.4
            enemy_y[i] += enemyy_change[i]

    
        # Collision
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('sound/explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
        
        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 500
        bullet_state = 'ready'

    if  bullet_state == 'fire':
        bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
