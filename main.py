import pygame
import os
import numpy as np

pygame.init()

# base appearance settings:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# base game settings:
FPS = 60
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
pygame.display.set_caption("Walking man")  # app title

# load images:
WALKING_RIGHT = pygame.image.load(os.path.join("Assets", "walking_right.png"))
WALKING_LEFT = pygame.image.load(os.path.join("Assets", "walking_left.png"))
WALKING_STAND = pygame.image.load(os.path.join("Assets", "walking_stand.png"))
# WALKING_STAND = pygame.image.load(os.path.join("Assets", "walking_stand_ground.png"))
BACKGROUND = pygame.image.load(os.path.join("Assets", "background.png"))
WALL_1 = pygame.image.load(os.path.join("Assets", "wall_left_bottom.png"))
WALL_2 = pygame.image.load(os.path.join("Assets", "wall_right_bottom.png"))
WALL_3 = pygame.image.load(os.path.join("Assets", "wall_left_top.png"))
WALL_4 = pygame.image.load(os.path.join("Assets", "wall_right_top.png"))
BRIDGE = pygame.image.load(os.path.join("Assets", "bridge.png"))

OBSTACLES = [
    # edges:
    pygame.Rect(0, 0, 10, HEIGHT),
    pygame.Rect(0, 0, WIDTH, 20),
    pygame.Rect(0, HEIGHT-20, WIDTH, 20), 
    pygame.Rect(WIDTH-10, 1, 10, HEIGHT),
    # other objects:
    pygame.Rect(644, 32, 49, 323),
    pygame.Rect(644, 430, 49, 237),
    pygame.Rect(167, 31, 49, 228),
    pygame.Rect(167, 336, 49, 156),
    pygame.Rect(148, 446, 67, 46),
    pygame.Rect(438, 0, 118, 110),
    pygame.Rect(438, 163, 118, 380),
    pygame.Rect(438, 595, 118, 120),
    pygame.Rect(0, 0, 500, 50),
    pygame.Rect(0, 0, 150, 115),
    pygame.Rect(0, 115, 70, 30),
    pygame.Rect(0, 145, 40, 30),
    pygame.Rect(0, 420, 40, 30),
    pygame.Rect(0, 448, 142, 300),
    pygame.Rect(142, 640, 25, 100),
    pygame.Rect(275, 50, 55, 25),
]

class Character:
    def __init__(self, pic, name="John Doe", x=0, y=0, speed=2, rotation_speed=4, rotation=0, size=50):
        # self.__dict__.update(locals())
        self.pic, self.name, self.x, self.y, self.speed, self.rotation_speed, self.rotation, self.size = pic, name, x, \
            y, speed, rotation_speed, rotation, size
        self.walk_last_time = 0
        self.walk_start_time = None
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

class Player(Character):
    def move(self, keys_pressed):
        # rotation:
        if keys_pressed[pygame.K_a]:
            self.rotation += self.rotation_speed
        if keys_pressed[pygame.K_d]:
            self.rotation -= self.rotation_speed
        # movement with 'W': 
        if keys_pressed[pygame.K_w]:
            # animation:
            time_now = pygame.time.get_ticks()
            # the updating time in the walking images is tied to the character's speed:
            time_diff = (time_now - self.walk_start_time) / (500 / self.speed)
            time_diff_mod = np.mod(int(time_diff), 4)  # 3 possible states rotate in a 4 element cycle
            if time_diff_mod == 0:
                self.pic = WALKING_RIGHT
            elif (time_diff_mod == 1) or (time_diff_mod == 3):
                self.pic = WALKING_STAND
            else:
                self.pic = WALKING_LEFT

            # it will eventually move if some time passed since the last update (making it less smooth intentionally):
            if (pygame.time.get_ticks() - self.walk_last_time > (FPS * 0.6)):
                x_delta = -np.sin(self.rotation * np.pi / 180) * self.speed
                y_delta = -np.cos(self.rotation * np.pi / 180) * self.speed
                
                # create a temporary rectangle with the new positions and check if the move is valid:
                temp_rect = pygame.Rect(self.rect.x+x_delta, self.rect.y+y_delta, self.size, self.size)
                num_collides = np.sum([temp_rect.colliderect(obstacle) for obstacle in OBSTACLES])
                # if valid then move, else just stand at that point:
                if num_collides == 0:
                    self.rect.x += x_delta
                    self.rect.y += y_delta
                    self.x = self.rect.x
                    self.y = self.rect.y
                    self.walk_last_time = pygame.time.get_ticks()
                else:
                    self.pic = WALKING_STAND


def draw_window(player):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(WALL_1, (149, 336))
    WIN.blit(WALL_2, (644, 430))
    WIN.blit(WALL_3, (167, 31))
    WIN.blit(WALL_4, (644, 32))
    WIN.blit(BRIDGE, (430, 100))
    WIN.blit(BRIDGE, (430, 530))
    WIN.blit(reshape_and_rotate(player.pic, player.size, player.rotation), (player.x, player.y))
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
    player = Player(WALKING_STAND, name="John", x=300, y=300, speed=3, rotation_speed=4, rotation=0, size=35)
    WIN.blit(reshape_and_rotate(player.pic, player.size, player.rotation), (player.x, player.y))

    clock = pygame.time.Clock()
    run = True
    while run:
        # controlling FPS:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # quit game

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.walk_start_time = pygame.time.get_ticks()  # moving
                if event.key == pygame.K_LSHIFT:
                    player.speed *= 2  # running

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.pic = WALKING_STAND  # stop moving
                if event.key == pygame.K_LSHIFT:
                    player.speed /= 2  # stop running
        # move player:
        player.move(pygame.key.get_pressed())

        # draw window:
        draw_window(player)
        
        # draw obstacles:
        # for obstacle in OBSTACLES:
        #     pygame.draw.rect(WIN, RED, obstacle)
        # pygame.display.update()

if __name__ == '__main__':
    main()
