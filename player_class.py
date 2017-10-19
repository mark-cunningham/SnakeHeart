# Snake Heart
# Code Angel

# Classes: Player

import pygame

import screen
import utils

# Define constants
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_MOVE = 4


# Player class
class Player:

    # Class variables
    max_lives = 5
    max_spades = 3

    def __init__(self):

        # Load images
        self.player_still_image = utils.load_media('image', 'player_still')

        player_down_image = utils.load_media('image', 'player_down')
        player_down_alt_image = utils.load_media('image', 'player_down_alt')
        self.player_down_images = [player_down_image, player_down_alt_image]

        player_right_image = utils.load_media('image', 'player_right')
        player_right_alt_image = utils.load_media('image', 'player_right_alt')
        self.player_right_images = [player_right_image, player_right_alt_image]

        player_left_image = utils.load_media('image', 'player_left')
        player_left_alt_image = utils.load_media('image', 'player_left_alt')
        self.player_left_images = [player_left_image, player_left_alt_image]

        player_up_image = utils.load_media('image', 'player_up')
        player_up_alt_image = utils.load_media('image', 'player_up_alt')
        self.player_up_images = [player_up_image, player_up_alt_image]

        self.player_dig_image = utils.load_media('image', 'player_dig')
        self.skeleton_image = utils.load_media('image', 'skeleton')

        # Load audio
        self.dig_sound = utils.load_media('audio', 'dig')
        self.win_game_sound = utils.load_media('audio', 'win_game')
        self.lose_life_sound = utils.load_media('audio', 'lose_life')

        self.image = self.player_still_image
        self.rect = pygame.Rect(screen.SCREENWIDTH / 2, screen.SCREENHEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.direction = 'none'

        self.gold = 0
        self.lives = 5
        self.spades = 0

        self.sword = [False, False, False, False]
        self.alive = True
        self.game_over_win = False
        self.game_over_lose = False

        self.image_num = 0
        self.dig_timer = 0
        self.time_to_dig = 30
        self.skeleton_time = 0

    # Draw the player
    def draw(self, display):

        if self.direction == 'right':
            self.image = self.player_right_images[self.image_num]
            self.image_num += 1

        elif self.direction == 'left':
            self.image = self.player_left_images[self.image_num]
            self.image_num += 1

        elif self.direction == 'up':
            self.image = self.player_up_images[self.image_num]
            self.image_num += 1

        elif self.direction == 'down':
            self.image = self.player_down_images[self.image_num]
            self.image_num += 1

        elif self.dig_timer > 0:
            self.image = self.player_dig_image

        elif self.alive is False:
            self.image = self.skeleton_image

        else:
            self.image = self.player_still_image

        if self.image_num >= len(self.player_up_images):
            self.image_num = 0

        display.show_image(self.image, self.rect.x, self.rect.y)

    # Direction updated when the player presses a key (left, right, up, down)
    def set_direction(self, direction):
        self.direction = direction

    # Start digging if the player has pressed the space bar
    # Only if Lucy is not already digging, is still alive, and has at least 1 spade
    def start_digging(self):
        if self.dig_timer == 0 and self.alive is True and self.spades > 0:
            self.dig_sound.play()
            self.dig_timer = self.time_to_dig
            self.spades -= 1

    # Update dig timer
    def dig(self, game_map):
        self.dig_timer -= 1

        # Once the timer reaches 0, draw the trap
        if self.dig_timer == 0:
            game_map.add_trap()

    # The Map object has identified Lucy has walked into water
    def map_water(self):
        if self.alive is True:
            self.die()

    # The Map object has identified Lucy has collected a coin
    def map_gold(self):
        self.gold += 1

    # The Map object has identified Lucy has collected a heart
    def map_heart(self):
        self.lives += 1

    # The Map object has identified Lucy has collected a spade
    def map_spade(self):
        self.spades += 1

    # The Map object has identified Lucy has collected a sword part
    def map_sword(self, sword_number):
        self.sword[sword_number - 1] = True

    # The Map object has identified Lucy has walked up to the castle
    def map_castle(self):

        # The game will be won if:
        # All parts of the Snake Heart sword have been collected and
        # the game is not already over
        if all(sword_part is True for sword_part in self.sword) and self.game_over_win is False:
            self.game_over_win = True
            self.win_game_sound.play()

    # Test if Lucy has collided with a monster
    def check_collision(self, monster):
        if self.rect.colliderect(monster.rect) and self.alive is True:
            self.die()

    def die(self):
        self.lives -= 1
        self.alive = False
        self.lose_life_sound.play()

        if self.lives > 0:
            self.skeleton_time = 30
        else:
            self.game_over_lose = True

    def skeleton(self, game_map):
        self.skeleton_time -= 1

        if self.skeleton_time == 0 and self.lives > 0:
            self.alive = True

            # After a life has been lost, teleport to a new location
            game_map.portal_move()
