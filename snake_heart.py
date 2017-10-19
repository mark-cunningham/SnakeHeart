#!/usr/bin/python
# Snake Heart
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

import screen
import player_class
import monster
import map_class
import utils


# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
display = screen.Display()
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)


def main():

    # Create the player object
    lucy = player_class.Player()

    # Create the map object
    game_map = map_class.Map()

    # Get the level and load the correct map
    game_map.level = utils.intro(display)
    game_map.load_map()

    # Display game instructions
    utils.instructions(display)

    # Monster lists
    bumblers = []
    whizzers = []
    boxers = []

    # Set up number of each monster to be spawned based on the current level
    bumblers_spawn_start = 0
    whizzers_spawn_start = 0
    boxers_spawn_start = 0

    if game_map.level == 1:
        bumblers_spawn_start = 50
        whizzers_spawn_start = 50
        boxers_spawn_start = 50
    elif game_map.level == 2:
        bumblers_spawn_start = 150
        whizzers_spawn_start = 75
        boxers_spawn_start = 100

    # Spawn Bumblers
    for bumbler_count in range(bumblers_spawn_start):
        bumbler = monster.Bumbler(game_map.level)
        bumbler.spawn_location(game_map)
        bumblers.append(bumbler)

    # Spawn Whizzers
    for whizzer_count in range(whizzers_spawn_start):
        whizzer = monster.Whizzer(game_map.level)
        whizzer.spawn_location(game_map)
        whizzers.append(whizzer)

    # Spawn Boxers
    for boxer_count in range(boxers_spawn_start):
        boxer = monster.Boxer(game_map.level)
        boxer.spawn_location(game_map)
        boxers.append(boxer)

    # Main game loop
    while True:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            # Only allow keypress if lucy is not digging, alive and not game over
            if (lucy.dig_timer == 0 and
                    lucy.alive is True and
                    lucy.game_over_win is False and
                    lucy.game_over_lose is False):

                if key_pressed[pygame.K_LEFT]:
                    lucy.set_direction('left')
                    game_map.scroll('right')

                elif key_pressed[pygame.K_RIGHT]:
                    lucy.set_direction('right')
                    game_map.scroll('left')

                elif key_pressed[pygame.K_UP]:
                    lucy.set_direction('up')
                    game_map.scroll('down')

                elif key_pressed[pygame.K_DOWN]:
                    lucy.set_direction('down')
                    game_map.scroll('up')

                else:
                    lucy.set_direction('none')

                if key_pressed[pygame.K_SPACE]:
                    lucy.start_digging()

            else:
                lucy.set_direction('none')

            if key_pressed[pygame.K_RETURN] and lucy.game_over_win is True:
                main()

            if key_pressed[pygame.K_RETURN] and lucy.game_over_lose is True:
                main()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Move all the Bumblers, removing any that fall into a hole
        for bumbler in bumblers:
            bumbler.move(game_map)

            if bumbler.alive is False:
                bumblers.remove(bumbler)

        # Move all the Whizzers, removing any that fall into a hole
        for whizzer in whizzers:
            whizzer.move(game_map)

            if whizzer.alive is False:
                whizzers.remove(whizzer)

        # Move all the Boxers, removing any that fall into a hole
        for boxer in boxers:
            boxer.move(game_map)

            if boxer.alive is False:
                boxers.remove(boxer)

        # If Lucy is digging, update the timer
        if lucy.dig_timer > 0:
            lucy.dig(game_map)

        # If Lucy is a skeleton, update the timer
        if lucy.alive is False:
            lucy.skeleton(game_map)

        game_map.reset_change()

        # Draw the map, Lucy and any monsters
        game_map.draw(display)
        lucy.draw(display)

        for bumbler in bumblers:
            bumbler.draw(display)

        for whizzer in whizzers:
            whizzer.draw(display)

        for boxer in boxers:
            boxer.draw(display)

        # Check if Lucy has touched any items (extra lives, spades, portal, gold, sword, water, castle)
        game_map.check_player_loc(lucy)

        # If the player has teleported, the relative location of the monsters on the map must be updated
        if game_map.portal is True:
            for bumbler in bumblers:
                bumbler.portal(game_map.d_portal_x, game_map.d_portal_y)

            for whizzer in whizzers:
                whizzer.portal(game_map.d_portal_x, game_map.d_portal_y)

            for boxer in boxers:
                boxer.portal(game_map.d_portal_x, game_map.d_portal_y)

            game_map.portal = False

        # Check if Lucy chas collided with any monsters
        for bumbler in bumblers:
            lucy.check_collision(bumbler)

        for whizzer in whizzers:
            lucy.check_collision(whizzer)

        for boxer in boxers:
            lucy.check_collision(boxer)

        # Potentially spawn new monsters
        monster.Bumbler.spawn(bumblers, game_map)
        monster.Whizzer.spawn(whizzers, game_map)
        monster.Boxer.spawn(boxers, game_map)

        # Display scoreboard
        utils.display_scoreboard(display, font, lucy.gold, lucy.lives, lucy.spades, lucy.sword)

        if lucy.game_over_lose is True:
            display.show_image(display.game_over_lose_image, 110, 380)

        if lucy.game_over_win is True:
            display.show_image(display.game_over_win_image, 50, 380)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
