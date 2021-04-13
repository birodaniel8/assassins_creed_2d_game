import pygame
import os
import sys
import numpy as np
from game_config import WIDTH, HEIGHT, FPS, WHITE, BACKGROUND, WALL_LOCATIONS, BRIDGE_LOCATIONS, ARROW_LOCATION, \
    KING_LOCATION, WALL_1, WALL_2, WALL_3, WALL_4, BRIDGE, ARROW, FIGHT_CLOUD, KING, PLAYER_STAND, GUARD_STAND, \
    GUARD_DEAD, BUSH, VIEW_RANGE, STARTSCREEN
from character import Player, GuardStanding, GuardWalking, Bush
from utils import rotate_around_center, reshape_and_rotate, get_distance_and_angle

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Creed 2D")  # app title

# user generated events for guard alerts and for finding the king:
GUARD_ALERT = pygame.USEREVENT + 1  # these numbers are just identifiers
KING_FOUND = pygame.USEREVENT + 2


def draw_text(text):
    """Draw a text to the center of the screen"""
    text_to_draw = pygame.font.SysFont("comicsans", 100).render(text, 1, WHITE)
    WIN.blit(text_to_draw, (WIDTH // 2 - text_to_draw.get_width() // 2, HEIGHT // 2 - text_to_draw.get_height() // 2))
    pygame.display.update()


def draw_window(player, guards, bushes):
    """Pygame window update function"""
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(WALL_1, WALL_LOCATIONS[0])
    WIN.blit(WALL_2, WALL_LOCATIONS[1])
    WIN.blit(WALL_3, WALL_LOCATIONS[2])
    WIN.blit(WALL_4, WALL_LOCATIONS[3])
    WIN.blit(BRIDGE, BRIDGE_LOCATIONS[0])
    WIN.blit(BRIDGE, BRIDGE_LOCATIONS[1])

    for guard in guards:
        WIN.blit(reshape_and_rotate(guard.pic, guard.size, guard.rotation), (guard.x, guard.y))
        # if not killed or being killed, add the view range:
        if guard.killed_at is None:
            WIN.blit(reshape_and_rotate(VIEW_RANGE, guard.size * guard.view_range_scale, guard.rotation-180),
                     (guard.view_range_x, guard.view_range_y))

    # draw player:
    WIN.blit(reshape_and_rotate(player.pic, player.size, player.rotation), (player.x, player.y))

    # draw bushes:
    for bush in bushes:
        WIN.blit(reshape_and_rotate(bush.picture, bush.size, 0), (bush.x, bush.y))

    # draw arrow at the beginning:
    if player.x == 1200 and player.y == 570:
        WIN.blit(reshape_and_rotate(ARROW, 100, 0), ARROW_LOCATION)

    # player is hiding if he is under the bushes:
    if player.hiding:
        WIN.blit(reshape_and_rotate(ARROW, 35, player.rotation-90), (player.x, player.y))

    # interaction with guards:
    for guard in guards:
        # if the player meets with a living guard we create the fighting cloud and after a small time the guard is dead:
        if player.rect.collidepoint(guard.rect.center) > 0 and guard.alive:
            WIN.blit(reshape_and_rotate(FIGHT_CLOUD, 70, np.random.randint(180)),
                     (guard.x-guard.size/2, guard.y-guard.size/2))
            now_time = pygame.time.get_ticks()
            if guard.killed_at is None:
                guard.killed_at = now_time
            elif now_time - guard.killed_at > 200:
                guard.alive = False
                guard.pic = GUARD_DEAD

    # draw the king:
    WIN.blit(reshape_and_rotate(KING, 40, 270), KING_LOCATION)

    pygame.display.update()


def guard_alerts(player, guards):
    """Check if the guards see the player or any dead body. If so, raise an alert"""
    for guard in guards:
        distance, angle = get_distance_and_angle(player, guard)
        if guard.alive and guard.killed_at is None:
            # if the player is within view range (we cover a little bit less than the half circle, hence the 80 degrees)
            if not player.hiding and distance < 140 and angle < 80:
                pygame.event.post(pygame.event.Event(GUARD_ALERT))
            # this is really not an optimal or scalable solution to check all other guards for all guards but with just
            # a few of them it is ok for now
            for other_guard in guards:
                if other_guard != guard:
                    distance, angle = get_distance_and_angle(other_guard, guard)
                    # if the other guard is dead and within view range:
                    if other_guard.killed_at is not None and distance < 140 and angle < 80:
                        pygame.event.post(pygame.event.Event(GUARD_ALERT))


def king_found(player):
    """King is found event"""
    if player.rect.colliderect(pygame.Rect(40, 270, 60, 40)):
        pygame.event.post(pygame.event.Event(KING_FOUND))


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
        GuardStanding(GUARD_STAND, name="Guard_1", x=1075, y=570, rotation=90, size=35),
        GuardStanding(GUARD_STAND, name="Guard_2", x=1040, y=200, rotation=180, size=35),
        GuardWalking(GUARD_STAND, name="Guard_3", x=1040, y=250, rotation=0,
                     size=35, speed=3, moving_direction="vertical", target=400),
        GuardWalking(GUARD_STAND, name="Guard_4", x=710, y=120, rotation=270,
                     size=35, speed=3, moving_direction="horizontal", target=850),
        GuardWalking(GUARD_STAND, name="Guard_5", x=735, y=200, rotation=180,
                     size=35, speed=3, moving_direction="vertical", target=375),
        GuardStanding(GUARD_STAND, name="Guard_6", x=825, y=440, rotation=270, size=35),
        GuardWalking(GUARD_STAND, name="Guard_7", x=300, y=120, rotation=270,
                     size=35, speed=3, moving_direction="horizontal", target=625),
        GuardWalking(GUARD_STAND, name="Guard_8", x=300, y=550, rotation=270,
                     size=35, speed=3, moving_direction="horizontal", target=625),
        GuardWalking(GUARD_STAND, name="Guard_9", x=300, y=150, rotation=270,
                     size=35, speed=3, moving_direction="vertical", target=520),
        GuardStanding(GUARD_STAND, name="Guard_10", x=225, y=280, rotation=270, size=35),
    ]

    WIN.blit(STARTSCREEN, (0, 0))  # start screen
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    game_started = False
    while run:
        # controlling FPS:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # quit game
                sys.exit()

            # start the game with pressing Enter (return):
            if not game_started and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True

            if game_started:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.walk_start_time = pygame.time.get_ticks()  # moving
                    if event.key == pygame.K_x:
                        player.speed *= 2  # running

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player.pic = PLAYER_STAND  # stop moving
                    if event.key == pygame.K_x:
                        player.speed /= 2  # stop running

                # break the game if the player or a dead body was been detected:
                if event.type == GUARD_ALERT:
                    draw_text("YOU HAVE BEEN DETECTED!")
                    pygame.time.delay(3000)  # wait 3 sec
                    run = False

                # break the game (winning!) if the king has been found:
                if event.type == KING_FOUND:
                    draw_text("YOU HAVE FOUND THE KING!")
                    pygame.time.delay(6000)  # wait 3 sec
                    run = False

        if game_started:

            # move player:
            player.move(pygame.key.get_pressed())

            # move guards:
            for guard in guards:
                guard.move()

            # is the player hiding:
            player.hiding = True if np.sum([player.rect.colliderect(bush.rect) for bush in bushes]) > 0 else False

            # guard alerts:
            guard_alerts(player, guards)

            # is the king found:
            king_found(player)

            # draw window:
            draw_window(player, guards, bushes)

    # restart the game:
    main()


if __name__ == '__main__':
    main()
