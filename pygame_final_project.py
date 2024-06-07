#Credits -
#I used a tutorial video by Coding With Russ, called PyGame Street Fighter Style Fighting Game in Python using Pygame - Complete Tutorial
#The music was made by CodeManu on opengameart.org
#The cat fighter was made by dogchicken on opengameart.org
#The dog fighter with a gun (a remix of IsometricRobot's dog) was made by Gory Figment
    #The original dog fighter (a remix of dogchicken's cat) was made by IsometricRobot
#Links
    #https://www.youtube.com/watch?v=s5bd9KMSSW4
    #https://opengameart.org/content/cat-fighter-sprite-sheet
    #https://opengameart.org/content/dog-fighter-cat-fighter-remix-base-add-on-one
    #https://opengameart.org/content/dog-fighter-addon2-assault-rifle-kit
    #https://opengameart.org/content/platformer-game-music-pack

import pygame
from fighter import Fighter
from sys import exit

pygame.init()

#Game Window -
screen_width = 675
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fightinging")
clock = pygame.time.Clock()
bg_sound = pygame.mixer.Sound("Boss Theme.mp3")
bg_sound.set_volume(0.25)
bg_sound.play(loops = -1)

#Colors -
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#Define fighter variables
cat_size = 64
cat_scale = 4
cat_offset = [21, 29]
cat_data = [cat_size, cat_scale, cat_offset]
dog_size = 64
dog_scale = 4
dog_offset = [22, 29]
dog_data = [dog_size, dog_scale, dog_offset]

#Sprites -
#Background:
color = (68,186,236)
screen.fill(color)
pygame.display.flip()

#Health Bar:
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 1, y - 1, 302, 32))
    pygame.draw.rect(screen, RED, (x, y, 300, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 300 * ratio, 30))

#Ground:
ground_surface = pygame.image.load("Grassy_Ground.png").convert_alpha()
ground_surface = pygame.transform.scale(ground_surface, (700, 700))

#Fighters:
cat_spritesheet = pygame.image.load("sprite_base_addon_2012_12_14.png").convert_alpha()
dog_spritesheet = pygame.image.load("dog_gun_fighter.png").convert_alpha()

#Steps in Fighter Animation:
cat_animation_steps = [4, 8, 8, 10, 9, 7, 6, 8, 13, 10, 12, 6, 8, 8, 8]
dog_animation_steps = [4, 8, 8, 8, 8, 10, 6, 4, 9]

#Create two instances of fighters
fighter_1 = Fighter(1, 0, 287, False, cat_data, cat_spritesheet, cat_animation_steps)
fighter_2 = Fighter(2, 395, 287, True, dog_data, dog_spritesheet, dog_animation_steps)

#Game Loop -
while True:
    #Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill(color)
    screen.blit(ground_surface,(0,100))

    draw_health_bar(fighter_1.health, 5, 20)
    draw_health_bar(fighter_2.health, 370, 20)
    
    fighter_1.move(675, 500, screen, fighter_2)
    fighter_2.move(675, 500, screen, fighter_1)

    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    pygame.display.update()
    clock.tick(60)