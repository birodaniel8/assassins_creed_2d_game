import pygame
import numpy as np
from game_config import FPS, PLAYER_RIGHT, PLAYER_LEFT, PLAYER_STAND, GUARD_RIGHT, GUARD_LEFT, GUARD_STAND, \
    VIEW_RANGE, OBSTACLES

class Character:
    """Character class"""

    def __init__(self, pic, name="John Doe", x=0, y=0, speed=2, rotation_speed=4, rotation=0, size=35):
        self.pic, self.name, self.x, self.y, self.speed, self.rotation_speed, self.rotation, self.size = pic, name, x, \
            y, speed, rotation_speed, rotation, size
        self.walk_last_time = 0
        self.walk_start_time = None
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


class Player(Character):
    """Class for the playable character"""

    def __init__(self, pic, name, x, y, speed, rotation_speed, rotation, size):
        super().__init__(pic, name, x, y, speed, rotation_speed, rotation, size)
        self.hiding = False

    def move(self, keys_pressed):
        """Movement for the playable character"""
        # rotation:
        if keys_pressed[pygame.K_LEFT]:
            self.rotation += self.rotation_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rotation -= self.rotation_speed
        # movement with the up arrow':
        if keys_pressed[pygame.K_UP]:
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
                temp_rect = pygame.Rect(self.rect.x + x_delta, self.rect.y + y_delta, self.size, self.size)
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
        self.alive = True
        self.killed_at = None
        # view range scale and the (x, y) coordinates for the image positioning:
        self.view_range_scale = 8
        self.view_range_x = self.x + self.size / 2 - self.size * self.view_range_scale / 2
        self.view_range_y = self.y + self.size / 2 - self.size * self.view_range_scale / 2

    def move(self):
        pass


class GuardStanding(Guard):
    """Standing guard class"""


class GuardWalking(Guard):
    """Walking guard class"""

    def __init__(self, pic, name, x, y, rotation, size, speed, moving_direction, target):
        super().__init__(pic, name, x, y, rotation=rotation, size=size)
        # the walking guard will walk between (x1, y1) and (x2, y2) with some speed
        # the walking is implemented in a way that it can only move to horizontal or vertical direction
        if moving_direction == "horizontal":
            assert np.abs(target - x) > 100, "The distance between the end points must be larger than 100"
            self.x_1, self.y_1, self.x_2, self.y_2 = x, y, target, y
            self.target_rotation = 90 if self.x_1 > self.x_2 else 270
        elif moving_direction == "vertical":
            assert np.abs(target - y) > 100, "The distance between the end points must be larger than 100"
            self.x_1, self.y_1, self.x_2, self.y_2 = x, y, x, target
            self.target_rotation = 0 if self.y_1 > self.y_2 else 180
        else:
            print("Not a valid walking direction")
        self.speed = speed

        # these are auxiliary variables for the guard movement:
        self.at_targets = True
        self.at_start = True  # if we are just at the start we don't want the target_rotation switched

    def move(self):
        """Movement of the walking guard"""
        if self.killed_at is None:
            # rotate the guard if it is not at the target_rotation:
            if np.mod(self.rotation, 360) != self.target_rotation:
                self.rotation += self.speed
            else:
                if self.walk_start_time is None:
                    self.walk_start_time = pygame.time.get_ticks()  # moving
                # animation:
                time_now = pygame.time.get_ticks()
                time_diff = (time_now - self.walk_start_time) / (500 / self.speed)
                time_diff_mod = np.mod(int(time_diff), 4)  # 3 possible states rotate in a 4 element cycle
                if time_diff_mod == 0:
                    self.pic = GUARD_RIGHT
                elif (time_diff_mod == 1) or (time_diff_mod == 3):
                    self.pic = GUARD_STAND
                else:
                    self.pic = GUARD_LEFT
                if (pygame.time.get_ticks() - self.walk_last_time > (FPS * 0.6)):
                    # move if the guard is in the proper direction:
                    if self.target_rotation == 270:
                        self.x += self.speed
                    elif self.target_rotation == 90:
                        self.x -= self.speed
                    elif self.target_rotation == 180:
                        self.y += self.speed
                    else:
                        self.y -= self.speed
                    self.rect.x = self.x
                    self.rect.y = self.y
                    # move the view range too:
                    self.view_range_x = self.x + self.size / 2 - self.size * self.view_range_scale / 2
                    self.view_range_y = self.y + self.size / 2 - self.size * self.view_range_scale / 2
                    self.walk_last_time = pygame.time.get_ticks()

            # if we are not at the start and we have just collided with one of the end points now,
            # switch target rotation:
            if self.at_start == False and self.at_targets == False and \
                    (self.rect.collidepoint(self.x_1, self.y_1) or self.rect.collidepoint(self.x_2, self.y_2)):
                self.target_rotation = np.mod(self.target_rotation + 180, 360)
                self.at_targets = True
                self.walk_start_time = None
                self.pic = GUARD_STAND

            # set these variables to false if we are far from the end points:
            # this is probably not the nicest way to implement this
            # if the distance from any of the end points is larger than 50 we can say we have left these points
            # unfortunately this means that the end points must be at least 101 distance away from each other
            if (np.sqrt((self.x - self.x_1)**2 + (self.y - self.y_1)**2) > 50) and \
                    (np.sqrt((self.x - self.x_2)**2 + (self.y - self.y_2)**2) > 50):
                self.at_targets = False
                self.at_start = False


class Bush:
    """Bush class"""

    def __init__(self, picture, x, y, size):
        self.picture, self.x, self.y, self.size = picture, x, y, size
        # the bush rectangle is a third of the bush size to make the hiding more realistic:
        self.rect = pygame.Rect(self.x+self.size/3, self.y+self.size/3, self.size/3, self.size/3)
