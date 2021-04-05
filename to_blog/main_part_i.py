import pygame
import os
import sys

# base game settings:
FPS = 60
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Walking man")  # app title

# load image:
WALKING_STAND = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join("Assets", "walking_stand.png")), (50, 50)), 180)


def draw_window(image, x, y):
    WIN.fill((255, 255, 255))
    WIN.blit(image, (x, y))
    pygame.display.update()


def main():
    character_rect = pygame.Rect(100, 100, 50, 50)
    WIN.blit(WALKING_STAND, (character_rect.x, character_rect.y))

    clock = pygame.time.Clock()
    run = True
    while run:
        # controlling FPS:
        clock.tick(FPS)

        for event in pygame.event.get():
            # quit event:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # move the image:
        if pygame.key.get_pressed()[pygame.K_w]:
            character_rect.y += 1
            
        # draw window:
        draw_window(WALKING_STAND, character_rect.x, character_rect.y)


if __name__ == '__main__':
    main()
