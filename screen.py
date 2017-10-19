# Snake Heart
# Code Angel

# Classes: Display

import pygame

import utils

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
TILE_SIZE = 16


# Display class used to handle the images not relating to the map, player or monsters
class Display:
    def __init__(self):
        self.game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Snake Heart')

        self.intro_screen = utils.load_media('image', 'intro_screen')
        self.instructions_screen = utils.load_media('image', 'instructions_screen')
        self.game_over_win_image = utils.load_media('image', 'game_over_win')
        self.game_over_lose_image = utils.load_media('image', 'game_over_lose')

        self.scoreboard_image = utils.load_media('image', 'scoreboard')
        self.scoreboard_heart_image = utils.load_media('image', 'scoreboard_heart')
        self.scoreboard_no_heart_image = utils.load_media('image', 'scoreboard_no_heart')
        self.scoreboard_spade_image = utils.load_media('image', 'scoreboard_spade')
        self.scoreboard_no_spade_image = utils.load_media('image', 'scoreboard_no_spade')

        self.scoreboard_sword_images = []
        self.scoreboard_sword_images.append(utils.load_media('image', 'scoreboard_sword_1'))
        self.scoreboard_sword_images.append(utils.load_media('image', 'scoreboard_sword_2'))
        self.scoreboard_sword_images.append(utils.load_media('image', 'scoreboard_sword_3'))
        self.scoreboard_sword_images.append(utils.load_media('image', 'scoreboard_sword_4'))

        self.scoreboard_no_sword_images = []
        self.scoreboard_no_sword_images.append(utils.load_media('image', 'scoreboard_no_sword_1'))
        self.scoreboard_no_sword_images.append(utils.load_media('image', 'scoreboard_no_sword_2'))
        self.scoreboard_no_sword_images.append(utils.load_media('image', 'scoreboard_no_sword_3'))
        self.scoreboard_no_sword_images.append(utils.load_media('image', 'scoreboard_no_sword_4'))

    def show_image(self, image, x, y):
        self.game_screen.blit(image, [x, y])
