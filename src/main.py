from os.path import join
from random import randint

import pygame

# Init
pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# Import image | Join from os to make sure path is dynamic | convert the image for pygame
player_surf = pygame.image.load(join("..", "images", "player.png")).convert_alpha()
star_surf = pygame.image.load(join("..", "images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("..", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("..", "images", "laser.png")).convert_alpha()

# Rectangles
player_rect = player_surf.get_frect(center=((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2)))
meteor_rect = meteor_surf.get_frect(center=((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2)))
laser_rect = laser_surf.get_frect(bottomleft=(20, (WINDOW_HEIGHT - 20)))

# Player direction
player_direction = pygame.math.Vector2(1, -1)
player_speed = 100

# Star positions
star_positions = [
    (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(20)
]

# Main Loop
while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game
    display_surface.fill("darkgray")
    for position in star_positions:
        display_surface.blit(star_surf, position)
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)

    # player
    player_rect.center += player_direction * player_speed * dt
    display_surface.blit(player_surf, player_rect)
    if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
        player_direction.y *= -1
    elif player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        player_direction.x *= -1
    pygame.display.update()

pygame.quit()
