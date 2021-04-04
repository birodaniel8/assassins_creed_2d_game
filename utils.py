import pygame
import numpy as np


def rotate_around_center(image, angle):
    """Rotate an image while keeping its center and size"""
    rotation_rect = image.get_rect().copy()
    rotation_image = pygame.transform.rotate(image, angle)
    rotation_rect.center = rotation_image.get_rect().center
    rotation_image = rotation_image.subsurface(rotation_rect).copy()
    return rotation_image


def reshape_and_rotate(img, size, rotation):
    """Reshape and rotate an image around the center"""
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
