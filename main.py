import pygame
import os
import numpy as np

pygame.init()

# base appearance settings:
WHITE = (255, 255, 255)

# base game settings:
FPS = 60
WIDTH, HEIGHT = 847, 472
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Walking man")  # app title

# load images:
WALKING_RIGHT = pygame.image.load(os.path.join("Assets", "walking_right.png"))
WALKING_LEFT = pygame.image.load(os.path.join("Assets", "walking_left.png"))
WALKING_STAND = pygame.image.load(os.path.join("Assets", "walking_stand.png"))
# WALKING_STAND = pygame.image.load(os.path.join("Assets", "walking_stand_ground.png"))
BACKGROUND = pygame.image.load(os.path.join("Assets", "gta_background.jpg"))


class Character:
    def __init__(self, pic, name="Character_0", x=0, y=0, speed=2, rotation_speed=4, rotation=0, size=50):
        self.__dict__.update(locals())
        self.walk_lask_time = 0
        self.walk_start_time = None

    def move(self, keys_pressed):
        # rotation:
        if keys_pressed[pygame.K_a]:
            self.rotation += self.rotation_speed
        if keys_pressed[pygame.K_d]:
            self.rotation -= self.rotation_speed
        # move if 'W' is pressed and some time passed since the last update (making it less smooth intentionally):
        if keys_pressed[pygame.K_w] and (pygame.time.get_ticks() - self.walk_lask_time > (FPS * 0.6)):
            self.x -= np.sin(self.rotation * np.pi / 180) * self.speed
            self.y -= np.cos(self.rotation * np.pi / 180) * self.speed
            self.walk_lask_time = pygame.time.get_ticks()

    def is_walking(self):
        if (self.walk_lask_time is not None) and (self.walk_start_time is not None):
            time_now = pygame.time.get_ticks()
            # if walking, change the appearance accordingly:
            if time_now - self.walk_lask_time < 100:
                time_diff = (time_now - self.walk_start_time) / (500 / self.speed)
                time_diff_mod = np.mod(int(time_diff), 4)  # 3 possible states rotate in a 4 element cycle
                if time_diff_mod == 0:
                    self.pic = WALKING_RIGHT
                elif (time_diff_mod == 1) or (time_diff_mod == 3):
                    self.pic = WALKING_STAND
                else:
                    self.pic = WALKING_LEFT
            # if not walking, the appearance is just standing:
            else:
                self.pic = WALKING_STAND


def draw_window(character_0):
    # WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0, 0))
    # character_0_rect = pygame.Rect(character_0.x, character_0.y, character_0.size, character_0.size)
    WIN.blit(reshape_and_rotate(character_0.pic, character_0.size, character_0.rotation),
             (character_0.x, character_0.y))
    pygame.display.update()


def rotate_around_center(image, angle):
    """rotate an image while keeping its center and size"""
    rotation_rect = image.get_rect().copy()
    rotation_image = pygame.transform.rotate(image, angle)
    rotation_rect.center = rotation_image.get_rect().center
    rotation_image = rotation_image.subsurface(rotation_rect).copy()
    return rotation_image


def reshape_and_rotate(img, size, rotation):
    return rotate_around_center(pygame.transform.scale(img, (size, size)), rotation)


def main():
    character_0 = Character(WALKING_STAND, name="John", x=500, y=300, speed=3, rotation_speed=4, rotation=0, size=35)

    # character_0_rect = pygame.Rect(character_0.x, character_0.y, character_0.size, character_0.size)
    WIN.blit(reshape_and_rotate(character_0.pic, character_0.size, character_0.rotation),
             (character_0.x, character_0.y))

    clock = pygame.time.Clock()
    run = True
    while run:
        # controlling FPS:
        clock.tick(FPS)

        for event in pygame.event.get():
            # quit event:
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    character_0.walk_start_time = pygame.time.get_ticks()

        # move character_0:

        character_0.move(pygame.key.get_pressed())
        # is walking:
        character_0.is_walking()

        # draw window:
        draw_window(character_0)


if __name__ == '__main__':
    main()
