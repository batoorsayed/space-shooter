from os.path import join
from random import randint, uniform

import pygame
from pygame.sprite import Group


# Player Sprite | w/ Group object
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(join("..", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2)))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # Cooldown
        self.can_shoot = True
        self.laser_shot_time = 0
        self.cooldown_duration = 400

        # Mask
        #  self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt  # type: ignore

        # Shooting
        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, all_sprites, laser_sprites)  # type: ignore
            self.can_shoot = False
            self.laser_shot_time = pygame.time.get_ticks()
            laser_sound.play()

        # Initiates laser_timer up above
        self.laser_timer()


# Star Sprite
class Star(pygame.sprite.Sprite):
    def __init__(self, surface, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


# Laser Sprite
class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=position)

    def update(self, dt):
        self.rect.centery -= 400 * dt  # type: ignore
        if self.rect.bottom < 0:  # type: ignore
            self.kill()


# Meteor Sprite
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surface, position, *groups: Group) -> None:
        super().__init__(*groups)
        self.original_image = surface
        self.image = self.original_image
        self.rect = self.image.get_frect(center=position)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(20, 50)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt  # type: ignore
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        # Meteor Rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)  # type: ignore

# Explosions
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, position, *groups: Group) -> None:
        super().__init__(*groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=position)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

# Collisions
def collisions():
    global running
    global meteors_shot

    collision_sprites = pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    )
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()
            meteors_shot += 1

# Score
def display_score():
    global meteors_shot

    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(
        f"Score: {str(current_time + (meteors_shot * 10))}\n Meteors Shot: {str(meteors_shot)}",
        True,
        (240, 240, 240),
    )
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(30, 20).move(0, -8), 5, 10)
    display_surface.blit(text_surf, text_rect)

# Init
pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()
meteors_shot = 0


# Import image | Join from os to make sure path is dynamic | convert the image for pygame
laser_surface = pygame.image.load(join("..", "images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(join("..", "images", "meteor.png")).convert_alpha()
star_surface = pygame.image.load(join("..", "images", "star.png")).convert_alpha()
explosion_frames = [
    pygame.image.load(join("..", "images", "explosion", f"{i}.png")).convert_alpha()
    for i in range(21)
]

# Import Sound
laser_sound = pygame.mixer.Sound(join("..", "audio", "laser.wav"))
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(join("..", "audio", "explosion.wav"))
explosion_sound.set_volume(0.2)
game_music = pygame.mixer.Sound(join("..", "audio", "game_music.wav"))
game_music.set_volume(0.1)
game_music.play()

# Import Font
font = pygame.font.Font(join("..", "images", "Oxanium-Bold.ttf"), size=30)


# Create Sprite Group
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# Call Sprites
for i in range(20):
    Star(star_surface, all_sprites)
player = Player(all_sprites)

# Meteor Events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# Main Loop
while running:
    # Frame Control
    dt = clock.tick() / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x = randint(0, WINDOW_WIDTH)
            y = randint(-200, -100)
            Meteor(meteor_surface, (x, y), all_sprites, meteor_sprites)

    # Refresh
    all_sprites.update(dt)
    collisions()

    # Game
    display_surface.fill("#3a2e3f")
    display_score()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
