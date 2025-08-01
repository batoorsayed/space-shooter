from os.path import join
from random import randint

import pygame
from pygame.sprite import Group


# Player Sprite | w/ Group object
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            join("..", "images", "player.png")
        ).convert_alpha()
        self.rect = self.image.get_frect(
            center=((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))
        )
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * dt
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            print("pew")


# Star Sprite
class Star(pygame.sprite.Sprite):
    def __init__(self, *groups: Group, surface) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(join("..", "images", "star.png")).convert_alpha()
        self.image = surface
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


# Init
pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()


# Import image | Join from os to make sure path is dynamic | convert the image for pygame
meteor_surf = pygame.image.load(join("..", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("..", "images", "laser.png")).convert_alpha()

# Rectangles
meteor_rect = meteor_surf.get_frect(center=((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2)))
laser_rect = laser_surf.get_frect(bottomleft=(20, (WINDOW_HEIGHT - 20)))

# Create Sprite Group
all_sprites = pygame.sprite.Group()

# Call Sprites
star_surface = pygame.image.load(join("..", "images", "star.png")).convert_alpha()
for i in range(20):
    Star(all_sprites, surface=star_surface)
player = Player(all_sprites)

# Main Loop
while running:
    # Frame Control
    dt = clock.tick() / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game
    display_surface.fill("darkgray")

    # Objects
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    all_sprites.update(dt)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
