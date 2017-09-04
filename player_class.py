import pygame

import screen
import snake_heart
import utils

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_MOVE = 4

# Player class
class Player:

    max_lives = 5
    max_spades = 3

    def __init__(self):
        self.player_down_image = pygame.image.load("player_down.png").convert_alpha()
        player_down_image_b = pygame.image.load("player_down_b.png").convert_alpha()
        player_down_image_c = pygame.image.load("player_down_c.png").convert_alpha()
        self.player_down_images = [player_down_image_b, player_down_image_c]

        #self.player_right_image = pygame.image.load("player_right.png").convert()
        player_right_image_b = pygame.image.load("player_right_b.png").convert_alpha()
        player_right_image_c = pygame.image.load("player_right_c.png").convert_alpha()
        self.player_right_images = [player_right_image_b, player_right_image_c]

        #self.player_left_image = pygame.image.load("player_left.png").convert()
        player_left_image_b = pygame.image.load("player_left_b.png").convert_alpha()
        player_left_image_c = pygame.image.load("player_left_c.png").convert_alpha()
        self.player_left_images = [player_left_image_b, player_left_image_c]

        #player_up_image = pygame.image.load("player_up.png").convert()
        player_up_image_b = pygame.image.load("player_up_b.png").convert_alpha()
        player_up_image_c = pygame.image.load("player_up_c.png").convert_alpha()
        self.player_up_images = [player_up_image_b, player_up_image_c]

        self.player_dig_image = pygame.image.load("player_dig.png").convert_alpha()
        self.skeleton_image = pygame.image.load("skeleton.png").convert_alpha()

        self.dig_sound = utils.load_media('audio', 'dig')
        self.win_game_sound = utils.load_media('audio', 'win_game')
        self.lose_life_sound = utils.load_media('audio', 'lose_life')

        self.reset()

    def reset(self):

        self.image = self.player_down_image
        self.rect = self.image.get_rect()

        self.set_location([screen.SCREENWIDTH / 2, screen.SCREENHEIGHT / 2])
        self.set_direction('down')

        self.gold = 0
        #self.kills = 0
        self.lives = 5
        self.spades = 0
        #self.sword = [False, False, False, False]
        self.sword = [False, False, False, False]
        self.alive = True
        self.game_over_win = False
        self.game_over_lose = False

        self.image_num = 0
        self.dig_timer = 0
        self.time_to_dig = 30
        self.skeleton_time = 0



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
            self.image = self.player_down_image

        if self.image_num >= len(self.player_up_images):
            self.image_num = 0

        #game_screen.blit(self.image, [self.rect.x, self.rect.y])
        display.show_image(self.image, self.rect.x, self.rect.y)





    def set_location(self, location):
        x_coord = location[0]
        y_coord = location[1]
        self.rect = pygame.Rect(x_coord, y_coord, PLAYER_WIDTH, PLAYER_HEIGHT)

    """"def move(self, dx, dy):
        # Move the rectangle
        self.rect.x += dx
        self.rect.y += dy"""

    def set_direction(self, direction):
        self.direction = direction

    def start_digging(self):
        if self.dig_timer == 0 and self.alive is True and self.spades > 0:
            self.dig_sound.play()
            self.dig_timer = self.time_to_dig
            self.spades -= 1

    def dig(self, map):
        self.dig_timer -= 1

        if self.dig_timer == 0:
            map.add_trap()


    def map_water(self):
        if self.alive is True:
            self.die()

    def map_gold(self):
        self.gold += 1


    def map_heart(self):
        self.lives += 1


    def map_spade(self):
        self.spades+= 1


    def map_sword(self, sword_number):
        self.sword[sword_number - 1] = True


    def map_castle(self):
        if all(sword_part is True for sword_part in self.sword) and self.game_over_win is False:
            self.game_over_win = True
            self.win_game_sound.play()


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

    def skeleton(self, map):
        self.skeleton_time -= 1

        if self.skeleton_time == 0 and self.lives > 0:
            self.alive = True
            map.portal_move()

