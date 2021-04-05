import pygame
import os
import sys
import numpy as np

pygame.init()

# base appearance settings:
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# base game settings:
FPS = 60
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Walking man")  # app title

# load images:
PLAYER_RIGHT = pygame.image.load(os.path.join("Assets", "player_right.png"))
PLAYER_LEFT = pygame.image.load(os.path.join("Assets", "player_left.png"))
PLAYER_STAND = pygame.image.load(os.path.join("Assets", "player_stand.png"))
# PLAYER_STAND = pygame.image.load(os.path.join("Assets", "player_stand_ground.png"))
GUARD_RIGHT = pygame.image.load(os.path.join("Assets", "guard_right.png"))
GUARD_LEFT = pygame.image.load(os.path.join("Assets", "guard_left.png"))
GUARD_STAND = pygame.image.load(os.path.join("Assets", "guard_stand.png"))
VIEW_RANGE = pygame.image.load(os.path.join("Assets", "view_range.png"))
BACKGROUND = pygame.image.load(os.path.join("Assets", "background.png"))
WALL_1 = pygame.image.load(os.path.join("Assets", "wall_left_bottom.png"))
WALL_2 = pygame.image.load(os.path.join("Assets", "wall_right_bottom.png"))
WALL_3 = pygame.image.load(os.path.join("Assets", "wall_left_top.png"))
WALL_4 = pygame.image.load(os.path.join("Assets", "wall_right_top.png"))
BRIDGE = pygame.image.load(os.path.join("Assets", "bridge.png"))
ARROW = pygame.image.load(os.path.join("Assets", "arrow.png"))
BUSH = pygame.image.load(os.path.join("Assets", "bush.png"))

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
    pygame.Rect(550, 675, 30, 30),
    pygame.Rect(915, 220, 55, 310),
    pygame.Rect(950, 480, 50, 180),
    pygame.Rect(915, 610, 55, 310),
    pygame.Rect(1145, 20, 150, 30),
    pygame.Rect(1210, 50, 150, 30),
    pygame.Rect(1230, 80, 150, 20),
    pygame.Rect(1250, 80, 150, 40),
    pygame.Rect(1250, 345, 150, 30),
    pygame.Rect(1225, 370, 150, 30),
    pygame.Rect(1195, 400, 150, 30),
    pygame.Rect(1165, 430, 150, 30),
    pygame.Rect(1142, 460, 150, 40),
]

# user generated events for guard alerts:
GUARD_ALERT = pygame.USEREVENT + 1  # these numbers are just identifiers


class Character:
    def __init__(self, pic, name="John Doe", x=0, y=0, speed=2, rotation_speed=4, rotation=0, size=35):
        # self.__dict__.update(locals())
        self.pic, self.name, self.x, self.y, self.speed, self.rotation_speed, self.rotation, self.size = pic, name, x, \
            y, speed, rotation_speed, rotation, size
        self.walk_last_time = 0
        self.walk_start_time = None
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


class Player(Character):
    def __init__(self, pic, name, x, y, speed, rotation_speed, rotation, size):
        super().__init__(pic, name, x, y, speed, rotation_speed, rotation, size)
        self.hiding = False

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
                self.pic = PLAYER_RIGHT
            elif (time_diff_mod == 1) or (time_diff_mod == 3):
                self.pic = PLAYER_STAND
            else:
                self.pic = PLAYER_LEFT

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
                    self.pic = PLAYER_STAND


class Guard(Character):
    """Guard class"""

    def __init__(self, pic, name, x, y, rotation, size):
        super().__init__(pic, name, x, y, speed=0, rotation_speed=0, rotation=rotation, size=size)
        # view range scale and the (x, y) coordinates for the image positioning:
        self.view_range_scale = 8
        self.view_range_x = self.x + self.size / 2 - self.size * self.view_range_scale / 2
        self.view_range_y = self.y + self.size / 2 - self.size * self.view_range_scale / 2



class GuardStanding(Guard):
    """Standing guard class"""


class Bush:
    """Bush class"""

    def __init__(self, picture, x, y, size):
        self.picture, self.x, self.y, self.size = picture, x, y, size
        # the bush rectangle is a third of the bush size to make the hiding more realistic:
        self.rect = pygame.Rect(self.x+self.size/3, self.y+self.size/3, self.size/3, self.size/3)


def draw_window(player, guards, bushes):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(WALL_1, (149, 336))
    WIN.blit(WALL_2, (644, 430))
    WIN.blit(WALL_3, (167, 31))
    WIN.blit(WALL_4, (644, 32))
    WIN.blit(BRIDGE, (430, 100))
    WIN.blit(BRIDGE, (430, 530))
    
    for guard in guards:
        WIN.blit(reshape_and_rotate(guard.pic, guard.size, guard.rotation), (guard.x, guard.y))
        WIN.blit(reshape_and_rotate(VIEW_RANGE, guard.size * guard.view_range_scale, guard.rotation-180),
                (guard.view_range_x, guard.view_range_y))
    
    WIN.blit(reshape_and_rotate(player.pic, player.size, player.rotation), (player.x, player.y))
    
    for bush in bushes:
        WIN.blit(reshape_and_rotate(bush.picture, bush.size, 0), (bush.x, bush.y))
    
    if player.x == 1200 and player.y == 570:
        WIN.blit(reshape_and_rotate(ARROW, 100, 0), (1100, 535))
        
    if player.hiding:
        WIN.blit(reshape_and_rotate(ARROW, 35, player.rotation-90), (player.x, player.y))
        
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


def get_distance_and_angle(obj1, obj2):
    """Get the distance and the angle between two objects with a rectangle in their attributes using cosine law"""
    # applying cosine law:
    a_x, a_y = obj1.rect.centerx, obj1.rect.centery  # A: obj1 location
    c_x, c_y = obj2.rect.centerx, obj2.rect.centery  # C: obj2 location
    distance_ac = np.sqrt((a_x - c_x)**2 + (a_y - c_y)**2)  # distance between obj1 and obj2
    # generate an auxiliary point B at the direction of obj2 rotation with distance 100 from C:
    x_delta = -np.sin(obj2.rotation * np.pi / 180) * 100
    y_delta = -np.cos(obj2.rotation * np.pi / 180) * 100
    b_x, b_y = c_x + x_delta, c_y + y_delta  # B
    distance_bc = 100
    distance_ab = np.sqrt((a_x - b_x)**2 + (a_y - b_y)**2)
    # cosine law:
    angle = np.arccos((distance_bc**2 + distance_ac**2 - distance_ab**2) /
                      (2 * distance_bc * distance_ac)) * 180 / np.pi
    return distance_ac, angle


def guard_alerts(player, guards):
    """Check if the guards see the player or any dead body. If so, raise an alert"""
    for guard in guards:
        distance, angle = get_distance_and_angle(player, guard)
        # if the player is within view range (we cover a little bit less than the half circle, hence the 80 degrees)
        if not player.hiding and distance < 140 and angle < 80:
                pygame.event.post(pygame.event.Event(GUARD_ALERT))

def main():
    player = Player(PLAYER_STAND, name="John", x=1200, y=570, speed=3, rotation_speed=4, rotation=90, size=35)
    bushes = [Bush(BUSH, np.random.randint(1075, 1200), np.random.randint(100, 300), 50) for i in range(25)] + \
        [Bush(BUSH, np.random.randint(1075, 1150), np.random.randint(300, 350), 50) for i in range(5)] + \
        [Bush(BUSH, np.random.randint(700, 900), np.random.randint(25, 75), 50) for i in range(10)] + \
        [Bush(BUSH, np.random.randint(800, 850), np.random.randint(200, 350), 50) for i in range(15)] + \
        [Bush(BUSH, np.random.randint(700, 850), np.random.randint(575, 625), 50) for i in range(7)] + \
        [Bush(BUSH, np.random.randint(200, 230), np.random.randint(450, 650), 50) for i in range(12)] + \
        [Bush(BUSH, np.random.randint(225, 240), np.random.randint(100, 200), 50) for i in range(7)] + \
        [Bush(BUSH, np.random.randint(375, 400), np.random.randint(200, 450), 50) for i in range(10)]
    guards = [
        GuardStanding(GUARD_STAND, name="Guard_1", x=1075, y=570, rotation=90, size=35)
    ]

    clock = pygame.time.Clock()
    run = True
    while run:
        # controlling FPS:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # quit game
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.walk_start_time = pygame.time.get_ticks()  # moving
                if event.key == pygame.K_LSHIFT:
                    player.speed *= 2  # running

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.pic = PLAYER_STAND  # stop moving
                if event.key == pygame.K_LSHIFT:
                    player.speed /= 2  # stop running
            
            # break the game if the player has been detected:
            if event.type == GUARD_ALERT:
                pygame.time.delay(3000)  # wait 3 sec
                run = False
        # move player:
        player.move(pygame.key.get_pressed())

        # is the player hiding:
        player.hiding = True if np.sum([player.rect.colliderect(bush.rect) for bush in bushes]) > 0 else False

        # guard alerts:
        guard_alerts(player, guards)

        # draw window:
        draw_window(player, guards, bushes)
        
        # draw obstacles:
        # for obstacle in OBSTACLES:
        #     pygame.draw.rect(WIN, RED, obstacle)
        # pygame.display.update()

if __name__ == '__main__':
    main()
