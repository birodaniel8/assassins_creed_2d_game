import pygame
import os

# base appearance settings:
WHITE = (255, 255, 255)

# base game settings:
FPS = 60
WIDTH, HEIGHT = 1280, 720

# load images:
PLAYER_RIGHT = pygame.image.load(os.path.join("Assets", "player_right.png"))
PLAYER_LEFT = pygame.image.load(os.path.join("Assets", "player_left.png"))
PLAYER_STAND = pygame.image.load(os.path.join("Assets", "player_stand.png"))
GUARD_RIGHT = pygame.image.load(os.path.join("Assets", "guard_right.png"))
GUARD_LEFT = pygame.image.load(os.path.join("Assets", "guard_left.png"))
GUARD_STAND = pygame.image.load(os.path.join("Assets", "guard_stand.png"))
GUARD_DEAD = pygame.image.load(os.path.join("Assets", "guard_dead.png"))
FIGHT_CLOUD = pygame.image.load(os.path.join("Assets", "fight_cloud.png"))
VIEW_RANGE = pygame.image.load(os.path.join("Assets", "view_range.png"))
STARTSCREEN = pygame.image.load(os.path.join("Assets", "start_screen.png"))
BACKGROUND = pygame.image.load(os.path.join("Assets", "background.png"))
WALL_1 = pygame.image.load(os.path.join("Assets", "wall_left_bottom.png"))
WALL_2 = pygame.image.load(os.path.join("Assets", "wall_right_bottom.png"))
WALL_3 = pygame.image.load(os.path.join("Assets", "wall_left_top.png"))
WALL_4 = pygame.image.load(os.path.join("Assets", "wall_right_top.png"))
BRIDGE = pygame.image.load(os.path.join("Assets", "bridge.png"))
ARROW = pygame.image.load(os.path.join("Assets", "arrow.png"))
BUSH = pygame.image.load(os.path.join("Assets", "bush.png"))
KING = pygame.image.load(os.path.join("Assets", "king.png"))

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

WALL_LOCATIONS = [
    (149, 336),
    (644, 430),
    (167, 31),
    (644, 32)
]

BRIDGE_LOCATIONS = [
    (430, 100),
    (430, 530)
]

ARROW_LOCATION = (1100, 535)

KING_LOCATION = (50, 275)