# Snake Heart
# © Code Angel 2017

import pygame, sys
from pygame.locals import *
import random
import csv
import gamedisplay


# Define the colours
WHITE = (255, 255, 255)
GREEN = (51, 223, 32)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
TILE_SIZE = 16

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_MOVE = 4


# Player class
class Player(object):

    max_lives = 5
    max_spades = 3

    def __init__(self):
        self.player_down_image = pygame.image.load("player_down.png").convert()
        player_down_image_b = pygame.image.load("player_down_b.png").convert()
        player_down_image_c = pygame.image.load("player_down_c.png").convert()
        self.player_down_images = [player_down_image_b, player_down_image_c]

        #self.player_right_image = pygame.image.load("player_right.png").convert()
        player_right_image_b = pygame.image.load("player_right_b.png").convert()
        player_right_image_c = pygame.image.load("player_right_c.png").convert()
        self.player_right_images = [player_right_image_b, player_right_image_c]

        #self.player_left_image = pygame.image.load("player_left.png").convert()
        player_left_image_b = pygame.image.load("player_left_b.png").convert()
        player_left_image_c = pygame.image.load("player_left_c.png").convert()
        self.player_left_images = [player_left_image_b, player_left_image_c]

        #player_up_image = pygame.image.load("player_up.png").convert()
        player_up_image_b = pygame.image.load("player_up_b.png").convert()
        player_up_image_c = pygame.image.load("player_up_c.png").convert()
        self.player_up_images = [player_up_image_b, player_up_image_c]

        self.player_dig_image = pygame.image.load("player_dig.png").convert()
        self.skeleton_image = pygame.image.load("skeleton.png").convert()

        self.reset()

    def reset(self):

        self.image = self.player_down_image
        self.rect = self.image.get_rect()

        self.set_location([SCREENWIDTH / 2, SCREENHEIGHT / 2])
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



    def draw(self):
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

        game_screen.blit(self.image, [self.rect.x, self.rect.y])




    def set_location(self, location):
        x_coord = location[0]
        y_coord = location[1]
        self.rect = pygame.Rect(x_coord, y_coord, PLAYER_WIDTH, PLAYER_HEIGHT)

    """def move(self, dx, dy):
        # Move the rectangle
        self.rect.x += dx
        self.rect.y += dy"""

    def set_direction(self, direction):
        self.direction = direction

    def start_digging(self):
        if self.dig_timer == 0 and self.alive is True and self.spades > 0:
            self.dig_timer = self.time_to_dig
            self.spades -= 1

    def dig(self, map):
        if self.dig_timer > 0:
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
        if all(sword_part is True for sword_part in self.sword):
            self.game_over_win = True


    def check_collision(self, monster):
        if self.rect.colliderect(monster.rect) and self.alive is True:
            self.die()

    def die(self):
        self.lives -= 1
        self.alive = False
        if self.lives > 0:
            self.skeleton_time = 30
        else:
            self.game_over_lose = True

    def skeleton(self, map):
        if self.alive is False:
            self.skeleton_time -= 1

            if self.skeleton_time == 0 and self.lives > 0:
                self.alive = True
                map.portal_move()






# Map class
class Map(object):

    def __init__(self):
        self.water_image = pygame.image.load("water.png").convert()
        self.land_image = pygame.image.load("land.png").convert()
        self.portal_image = pygame.image.load("portal.png").convert()
        self.re_port_image = pygame.image.load("re-port.png").convert()
        self.beach_image = pygame.image.load("beach.png").convert()
        self.gold_image = pygame.image.load("gold.png").convert()
        self.trap_image = pygame.image.load("hole.png").convert()
        self.heart_image = pygame.image.load("heart.png").convert()
        self.spade_image = pygame.image.load("spade.png").convert()

        self.sword_1_image = pygame.image.load("sword_1.png").convert()
        self.sword_2_image = pygame.image.load("sword_2.png").convert()
        self.sword_3_image = pygame.image.load("sword_3.png").convert()
        self.sword_4_image = pygame.image.load("sword_4.png").convert()

        self.castle_1_image = pygame.image.load("castle_1.png").convert()
        self.castle_2_image = pygame.image.load("castle_2.png").convert()
        self.castle_3_image = pygame.image.load("castle_3.png").convert()
        self.castle_4_image = pygame.image.load("castle_4.png").convert()
        self.castle_5_image = pygame.image.load("castle_5.png").convert()
        self.castle_6_image = pygame.image.load("castle_6.png").convert()

        self.map_key = {'w': 'water',
                   'l': 'land',
                   'p': 'portal',
                   'r': 're-port',
                   'b': 'beach',
                   'g': 'gold',
                   't': 'trap',
                   'h': 'heart',
                   'd': 'spade',
                   '1': 'sword 1',
                   '2': 'sword 2',
                   '3': 'sword 3',
                   '4': 'sword 4',
                   'c1': 'castle 1',
                   'c2': 'castle 2',
                   'c3': 'castle 3',
                   'c4': 'castle 4',
                   'c5': 'castle 5',
                   'c6': 'castle 6',
                        }



        self.screen_cols = int(SCREENWIDTH / TILE_SIZE)
        self.screen_rows = int(SCREENHEIGHT / TILE_SIZE)

        self.map_tile_x = 0
        self.map_tile_y = 0
        self.map_tile_step_x = 0
        self.map_tile_step_y = 0

        self.player_row = int(SCREENHEIGHT / TILE_SIZE/ 2 + 1)
        self.player_col_left = int(SCREENWIDTH / TILE_SIZE / 2)
        self.player_col_right = int(SCREENWIDTH / TILE_SIZE / 2 + 1)

        self.dx = 0
        self.dy = 0

        self.portal = False
        self.d_portal_x = 0
        self.d_portal_y = 0

        self.level = 0





    def load_map(self):

        map_file = ''

        if self.level == 1:
            map_file = 'snakeheart map level 1.csv'
        elif self.level == 2:
            map_file = 'snakeheart map level 2.csv'

        with open(map_file, 'r') as csvfile:
            read_map = csv.reader(csvfile)
            self.tile_list = list(read_map)

        self.map_cols = len(self.tile_list[0])
        self.map_rows = len(self.tile_list)

        self.re_port_points = []
        self.find_re_port_points()


    def scroll(self, direction):

        self.dx = 0
        self.dy = 0

        if direction == 'right':
            if self.map_tile_x > 0:
                #self.map_tile_step_x += PLAYER_MOVE
                self.dx = PLAYER_MOVE
                self.dy = 0
        elif direction == 'left':
            if self.map_tile_x < self.map_cols - self.screen_cols - 1:
                #self.map_tile_step_x -= PLAYER_MOVE
                self.dx = -PLAYER_MOVE
                self.dy = 0
        elif direction == 'down':
            if self.map_tile_y > 0:
                #self.map_tile_step_y += PLAYER_MOVE
                self.dx = 0
                self.dy = PLAYER_MOVE
        elif direction == 'up':
            if self.map_tile_y < self.map_rows - self.screen_rows - 1:
                #self.map_tile_step_y -= PLAYER_MOVE
                self.dx = 0
                self.dy = -PLAYER_MOVE

        self.map_tile_step_x += self.dx
        self.map_tile_step_y += self.dy



        if self.map_tile_step_x >= TILE_SIZE:
            self.map_tile_step_x -= TILE_SIZE
            self.map_tile_x -= 1

        if self.map_tile_step_x < 0:
            self.map_tile_step_x += TILE_SIZE
            self.map_tile_x += 1

        if self.map_tile_step_y >= TILE_SIZE:
            self.map_tile_step_y -= TILE_SIZE
            self.map_tile_y -= 1

        if self.map_tile_step_y < 0:
            self.map_tile_step_y += TILE_SIZE
            self.map_tile_y += 1

    def draw(self):
        for row in range(self.screen_rows + 1):
            for col in range(self.screen_cols + 1):
                tile = self.map_key.get(self.tile_list[row + self.map_tile_y][col + self.map_tile_x])
                display_image = ''

                if tile == 'water':
                    display_image = self.water_image
                elif tile == 'land':
                    display_image = self.land_image
                elif tile == 'portal':
                    display_image = self.portal_image
                elif tile == 're-port':
                    display_image = self.re_port_image
                elif tile == 'gold':
                    display_image = self.gold_image
                elif tile == 'beach':
                    display_image = self.beach_image
                elif tile == 'trap':
                    display_image = self.trap_image
                elif tile == 'heart':
                    display_image = self.heart_image
                elif tile == 'spade':
                    display_image = self.spade_image

                elif tile == 'sword 1':
                    display_image = self.sword_1_image
                elif tile == 'sword 2':
                    display_image = self.sword_2_image
                elif tile == 'sword 3':
                    display_image = self.sword_3_image
                elif tile == 'sword 4':
                    display_image = self.sword_4_image

                elif tile == 'castle 1':
                    display_image = self.castle_1_image
                elif tile == 'castle 2':
                    display_image = self.castle_2_image
                elif tile == 'castle 3':
                    display_image = self.castle_3_image
                elif tile == 'castle 4':
                    display_image = self.castle_4_image
                elif tile == 'castle 5':
                    display_image = self.castle_5_image
                elif tile == 'castle 6':
                    display_image = self.castle_6_image

                game_screen.blit(display_image, [(col - 1) * TILE_SIZE + self.map_tile_step_x,
                                                 (row - 1) * TILE_SIZE + self.map_tile_step_y])
    def reset_change(self):
        self.dx = 0
        self.dy = 0

    def check_player_loc(self, player):
        tile_left = self.map_key.get(self.tile_list[self.player_row + self.map_tile_y + 1][self.player_col_left + self.map_tile_x])
        tile_right = self.map_key.get(self.tile_list[self.player_row + self.map_tile_y + 1][self.player_col_right + self.map_tile_x])

        touching_water = self.player_touching('water', tile_left, tile_right)
        touching_gold = self.player_touching('gold', tile_left, tile_right)
        touching_portal = self.player_touching('portal', tile_left, tile_right)
        touching_heart = self.player_touching('heart', tile_left, tile_right)
        touching_spade = self.player_touching('spade', tile_left, tile_right)

        touching_sword_1 = self.player_touching('sword 1', tile_left, tile_right)
        touching_sword_2 = self.player_touching('sword 2', tile_left, tile_right)
        touching_sword_3 = self.player_touching('sword 3', tile_left, tile_right)
        touching_sword_4 = self.player_touching('sword 4', tile_left, tile_right)

        touching_castle_1 = self.player_touching('castle 1', tile_left, tile_right)
        touching_castle_2 = self.player_touching('castle 2', tile_left, tile_right)
        touching_castle_3 = self.player_touching('castle 3', tile_left, tile_right)
        touching_castle_4 = self.player_touching('castle 4', tile_left, tile_right)
        touching_castle_5 = self.player_touching('castle 5', tile_left, tile_right)
        touching_castle_6 = self.player_touching('castle 6', tile_left, tile_right)

        if touching_water is True:
            player.map_water()
        elif touching_gold is True:
            player.map_gold()
            self.remove_item('gold', tile_left, tile_right)
        elif touching_heart is True:
            if player.lives < player.max_lives:
                player.map_heart()
                self.remove_item('heart', tile_left, tile_right)
        elif touching_spade is True:
            if player.spades < player.max_spades:
                player.map_spade()
                self.remove_item('spade', tile_left, tile_right)
        elif touching_portal is True:
            self.portal_move()

        elif touching_sword_1 is True:
            player.map_sword(1)
            self.remove_item('sword 1', tile_left, tile_right)
        elif touching_sword_2 is True:
            player.map_sword(2)
            self.remove_item('sword 2', tile_left, tile_right)
        elif touching_sword_3 is True:
            player.map_sword(3)
            self.remove_item('sword 3', tile_left, tile_right)
        elif touching_sword_4 is True:
            player.map_sword(4)
            self.remove_item('sword 4', tile_left, tile_right)

        elif touching_castle_1 is True:
            player.map_castle()
        elif touching_castle_2 is True:
            player.map_castle()
        elif touching_castle_3 is True:
            player.map_castle()
        elif touching_castle_4 is True:
            player.map_castle()
        elif touching_castle_5 is True:
            player.map_castle()
        elif touching_castle_6 is True:
            player.map_castle()


    def add_trap(self):
        self.add_trap_piece(self.player_row + self.map_tile_y, self.player_col_left + self.map_tile_x)
        self.add_trap_piece(self.player_row + self.map_tile_y, self.player_col_left + self.map_tile_x + 1)
        self.add_trap_piece(self.player_row + self.map_tile_y, self.player_col_left + self.map_tile_x + 2)
        self.add_trap_piece(self.player_row + self.map_tile_y + 1, self.player_col_left + self.map_tile_x)
        self.add_trap_piece(self.player_row + self.map_tile_y + 1, self.player_col_left + self.map_tile_x + 1)
        self.add_trap_piece(self.player_row + self.map_tile_y + 1, self.player_col_left + self.map_tile_x + 2)

    def add_trap_piece(self, row_tile, col_tile):
        if self.tile_list[row_tile][col_tile] == 'l':
            self.tile_list[row_tile][col_tile] = 't'


    def portal_move(self):
        random_re_port = random.choice(self.re_port_points)
        new_map_x = random_re_port[1] - 20
        new_map_y = random_re_port[0] - 15 - 2

        self.d_portal_x = self.map_tile_x - new_map_x
        self.d_portal_y = self.map_tile_y - new_map_y
        self.map_tile_x = new_map_x
        self.map_tile_y = new_map_y
        self.map_tile_step_x = 0
        self.map_tile_step_y = 0

        self.portal = True

    def find_re_port_points(self):
        for row in range(self.map_rows):
            for col in range(self.map_cols):
                tile = self.map_key.get(self.tile_list[row][col])

                if tile == 're-port':
                    self.re_port_points.append([row, col])




    def player_touching(self, item, tile_left, tile_right):
        player_touching_item = False
        if (tile_left == item and self.map_tile_step_x > PLAYER_MOVE) or tile_right == item:
            player_touching_item = True

        return player_touching_item

    def remove_item(self, item, tile_left, tile_right):
        if (tile_left == item and self.map_tile_step_x > PLAYER_MOVE):
            self.tile_list[self.player_row + self.map_tile_y + 1][self.player_col_left + self.map_tile_x] = 'l'
        elif tile_right == item:
            self.tile_list[self.player_row + self.map_tile_y + 1][self.player_col_right+ self.map_tile_x] = 'l'



class Monster(object):

    def __init__(self, image, speed):#, random_direction, intelligence):

        self.monster_image = pygame.image.load(image).convert()

        self.rect = self.monster_image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.speed = speed

        #self.random_direction = random_direction
        #self.intelligence = intelligence

        self.alive = True

        self.terrain_type_1 = ''
        self.terrain_type_2 = ''
        self.terrain_type_3 = ''
        self.terrain_type_4 = ''

    def standard_direction(self):
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def diagonal_direction(self):
        self.direction = random.choice(['up right', 'down right', 'down left', 'up left'])

    def spawn_location(self, map):

        start_tile_col = random.randint(0, map.map_cols - 1)
        start_tile_row = random.randint(0, map.map_rows - 1)

        terrain = map.map_key.get(map.tile_list[start_tile_row][start_tile_col])
        while terrain != 'land':
            start_tile_col = random.randint(0, map.map_cols - 1)
            start_tile_row = random.randint(0, map.map_rows - 1)

            terrain = map.map_key.get(map.tile_list[start_tile_row][start_tile_col])

        self.rect.x = (start_tile_col - map.map_tile_x) * TILE_SIZE
        self.rect.y = (start_tile_row - map.map_tile_y) * TILE_SIZE






    def draw(self):
        if self.alive is True:
            gamedisplay.blit_sprite(self.monster_image, self.rect.x, self.rect.y)
            #game_screen.blit(self.monster_image, [self.rect.x, self.rect.y])

    def move(self, map):
        if self.alive is True:
            if 'right' in self.direction:
                self.rect.x += self.speed
            if 'left' in self.direction:
                self.rect.x -= self.speed
            if 'down' in self.direction:
                self.rect.y += self.speed
            if 'up' in self.direction:
                self.rect.y -= self.speed


            self.rect.x += map.dx
            self.rect.y += map.dy

            self.update_surrounding_terrain(map)
            self.check_for_hole()
            self.check_if_drowned()
            self.maybe_change_direction()




    def update_surrounding_terrain(self, map):
        monster_tile_x_1 = int(self.rect.x / TILE_SIZE) + 1
        monster_tile_x_2 = int((self.rect.x + self.rect.width) / TILE_SIZE) + 1
        monster_tile_y_1 = int(self.rect.y / TILE_SIZE) + 1
        monster_tile_y_2 = int((self.rect.y + self.rect.height) / TILE_SIZE) + 1



        self.terrain_type_1 = map.map_key.get(map.tile_list[map.map_tile_y + monster_tile_y_1][map.map_tile_x + monster_tile_x_1])
        self.terrain_type_2 = map.map_key.get(map.tile_list[map.map_tile_y + monster_tile_y_1][map.map_tile_x + monster_tile_x_2])
        self.terrain_type_3 = map.map_key.get(map.tile_list[map.map_tile_y + monster_tile_y_2][map.map_tile_x + monster_tile_x_1])
        self.terrain_type_4 = map.map_key.get(map.tile_list[map.map_tile_y + monster_tile_y_2][map.map_tile_x + monster_tile_x_2])


    def check_for_hole(self):
        if self.alive is True:
            if self.terrain_type_1 == 'trap' or self.terrain_type_2 == 'trap' or self.terrain_type_3 == 'trap' or self.terrain_type_4 == 'trap':
                self.alive = False
                self.update_kills()

    def update_kills(self):
        pass


    def check_if_drowned(self):
        if self.alive is True:
            if self.terrain_type_1 == 'water' or self.terrain_type_2 == 'water' or self.terrain_type_3 == 'water' or self.terrain_type_4 == 'water':
                self.alive = False

    def maybe_change_direction(self):
        pass

    def portal(self, portal_x, portal_y):
        self.rect.x += portal_x * TILE_SIZE
        self.rect.y += portal_y * TILE_SIZE


class Bumbler(Monster):

    spawn_chance = 250
    kills = 0
    max = 100

    def __init__(self, level):
        speed = 0
        self.random_direction = 0
        self.intelligence = 0

        if level == 1:
            self.random_direction = 30
            self.intelligence = 5
            speed = 1
        elif level == 2:
            self.random_direction = 20
            self.intelligence = 3
            speed = 2

        super().__init__("monster_down.png", speed)
        super().standard_direction()


    @staticmethod
    def spawn(bumblers, map):
        spawn_chance = random.randint(1, Bumbler.spawn_chance)
        if spawn_chance == 1 and len(bumblers) < Bumbler.max:
            bumbler = Bumbler(map.level)
            bumbler.spawn_location(map)
            bumblers.append(bumbler)

    def update_kills(self):
        Bumbler.kills += 1



    def maybe_change_direction(self):
        # chance change is the chance of changing direction
        chance_change = random.randint(1, self.random_direction)
        if chance_change == 1:
            # smart change is going in the direction of player
            # lower intelligence, greater chance of a smart change rather than random
            smart_change = random.randint(1, self.intelligence)
            if smart_change == 1:
                if self.rect.y < SCREENHEIGHT / 2:
                    self.direction = 'down'
                else:
                    self.direction = 'up'
            elif smart_change == 2:
                if self.rect.x < SCREENWIDTH / 2:
                    self.direction = 'right'
                else:
                    self.direction = 'left'


class Whizzer(Monster):

    spawn_chance = 200
    kills = 0
    max = 30

    def __init__(self, level):
        speed = 0

        if level == 1:
            speed = 6
        elif level == 2:
            speed = 10

        super().__init__("whizzer_down.png", speed)
        super().standard_direction()

    @staticmethod
    def spawn(whizzers, map):
        spawn_chance = random.randint(1, Whizzer.spawn_chance)
        if spawn_chance == 1 and len(whizzers) < Whizzer.max:
            whizzer = Whizzer(map.level)
            whizzer.spawn_location(map)
            whizzers.append(whizzer)

    def update_kills(self):
        Whizzer.kills += 1



class Boxer(Monster):

    spawn_chance = 500
    kills = 0
    max = 70

    def __init__(self, level):
        self.random_direction = 0
        speed = 0

        if level == 1:
            self.random_direction = 15
            speed = 3
        elif level == 2:
            self.random_direction = 5
            speed = 5

        super().__init__("boxer_down.png", speed)
        super().diagonal_direction()
        #Monster.__init__(self, "boxer_down.png", speed)

    def maybe_change_direction(self):
        # chance change is the chance of changing direction
        chance_change = random.randint(1, self.random_direction)
        if chance_change == 1:
            if self.direction == 'up right':
                self.direction =  'down right'
            elif self.direction == 'down right':
                self.direction = 'down left'
            elif self.direction == 'down left':
                self.direction = 'up left'
            else:
                self.direction = 'up right'

    @staticmethod
    def spawn(boxers, map):
        spawn_chance = random.randint(1, Boxer.spawn_chance)
        if spawn_chance == 1 and len(boxers) < Boxer.max:
            boxer = Boxer(map.level)
            boxer.spawn_location(map)
            boxers.append(boxer)

    def update_kills(self):
        Boxer.kills += 1





def main():

    player = Player()
    map = Map()

    map.level = intro()
    map.load_map()


    bumblers = []
    whizzers = []
    boxers = []

    bumblers_spawn_start = 0
    whizzers_spawn_start = 0
    boxers_spawn_start = 0

    if map.level == 1:
        bumblers_spawn_start = 3
        whizzers_spawn_start = 2
        boxers_spawn_start = 4
    elif map.level == 2:
        bumblers_spawn_start = 10
        whizzers_spawn_start = 10
        boxers_spawn_start = 10



    for bumbler_count in range(bumblers_spawn_start):
        bumbler = Bumbler(map.level)
        bumbler.spawn_location(map)
        bumblers.append(bumbler)

    for whizzer_count in range(whizzers_spawn_start):
        whizzer = Whizzer(map.level)
        whizzer.spawn_location(map)
        whizzers.append(whizzer)

    for boxer_count in range(boxers_spawn_start):
        boxer = Boxer(map.level)
        boxer.spawn_location(map)
        boxers.append(boxer)


    while True:  # main game loop
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if player.dig_timer == 0 and player.alive is True and player.game_over_win is False and player.game_over_lose is False:

                if key_pressed[pygame.K_LEFT]:
                    #player.move(-PLAYER_MOVE, 0)
                    player.set_direction('left')
                    map.scroll('right')

                elif key_pressed[pygame.K_RIGHT]:
                    #player.move(PLAYER_MOVE, 0)
                    player.set_direction('right')
                    map.scroll('left')

                elif key_pressed[pygame.K_UP]:
                    #player.move(0, -PLAYER_MOVE)
                    player.set_direction('up')
                    map.scroll('down')

                elif key_pressed[pygame.K_DOWN]:
                    #player.move(0, PLAYER_MOVE)
                    player.set_direction('down')
                    map.scroll('up')


                else:
                    player.set_direction('none')

                if key_pressed[pygame.K_SPACE]:
                    player.start_digging()

            else:
                player.set_direction('none')

            if key_pressed[pygame.K_RETURN] and player.game_over_win is True:
                main()

            if key_pressed[pygame.K_RETURN] and player.game_over_lose is True:
                main()


            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for bumbler in bumblers:
            bumbler.move(map)
            if bumbler.alive is False:
                #player.kills += 1
                bumblers.remove(bumbler)
            #bumbler.maybe_change_direction()
            #bumbler.check_if_drowned()

        for whizzer in whizzers:
            whizzer.move(map)
            if whizzer.alive is False:
                #player.kills += 1
                whizzers.remove(whizzer)
            #whizzer.check_if_drowned()

        for boxer in boxers:
            boxer.move(map)
            if boxer.alive is False:
                #player.kills += 1
                boxers.remove(boxer)


        player.dig(map)
        player.skeleton(map)
        map.reset_change()

        map.draw()
        player.draw()

        for bumbler in bumblers:
            bumbler.draw()

        for whizzer in whizzers:
            whizzer.draw()

        for boxer in boxers:
            boxer.draw()


        map.check_player_loc(player)

        if map.portal is True:
            for bumbler in bumblers:
                bumbler.portal(map.d_portal_x, map.d_portal_y)

            for whizzer in whizzers:
                whizzer.portal(map.d_portal_x, map.d_portal_y)

            for boxer in boxers:
                boxer.portal(map.d_portal_x, map.d_portal_y)

            map.portal = False

        for bumbler in bumblers:
            player.check_collision(bumbler)

        for whizzer in whizzers:
            player.check_collision(whizzer)

        for boxer in boxers:
            player.check_collision(boxer)

        Bumbler.spawn(bumblers, map)
        Whizzer.spawn(whizzers, map)
        Boxer.spawn(boxers, map)


        display_scoreboard(player.gold, player.lives, player.spades, player.sword)

        if player.game_over_lose is True:
            game_screen.blit(game_over_lose_image, [110, 380])

        if player.game_over_win is True:
            game_screen.blit(game_over_win_image, [50, 380])


        pygame.display.update()
        clock.tick(30)

def display_scoreboard(gold, lives, spades, sword):
    text_y = 3
    gold_text_x = 28
    kills_text_x = 96
    score_text_x = 164
    hearts_x = 528
    spades_x = 428
    sword_x = 220
    icon_y = 3
    icon_gap = 20
    sword_gap = 18

    gold_score = 10
    bumbler_score = 20
    boxer_score = 30
    whizzer_score = 50

    #scoreboard_line = 20
    #scoreboard_colour = (0, 0, 0)

    #scoreboard_background_rect = (0, 0, SCREENWIDTH, scoreboard_line + 2 * scoreboard_margin)
    #pygame.draw.rect(game_screen, scoreboard_colour, scoreboard_background_rect)
    game_screen.blit(scoreboard_image, [0, 0])
    #game_screen.blit(map.gold_image, [scoreboard_margin, scoreboard_margin])

    text = font.render(str(gold), True, WHITE)
    game_screen.blit(text, [gold_text_x, text_y])

    total_kills = Bumbler.kills + Whizzer.kills + Boxer.kills
    text = font.render(str(total_kills), True, WHITE)
    game_screen.blit(text, [kills_text_x, text_y])

    total_score = gold * gold_score + Bumbler.kills * bumbler_score + Whizzer.kills * whizzer_score + Boxer.kills * boxer_score
    text = font.render(str(total_score), True, GREEN)
    game_screen.blit(text, [score_text_x, text_y])

    for heart in range(lives):
        game_screen.blit(scoreboard_heart_image, [hearts_x + heart * icon_gap, icon_y])

    for no_heart in range(lives, Player.max_lives):
        game_screen.blit(scoreboard_no_heart_image, [hearts_x + no_heart * icon_gap, icon_y])

    for spade in range(spades):
        game_screen.blit(scoreboard_spade_image, [spades_x + spade * icon_gap, icon_y])

    for no_spade in range(spades, Player.max_spades):
        game_screen.blit(scoreboard_no_spade_image, [spades_x + no_spade * icon_gap, icon_y])

    for sword_part_num, sword_part in enumerate(sword):
        if sword_part is True:
            game_screen.blit(scoreboard_sword_images[sword_part_num], [sword_x + sword_part_num * sword_gap, icon_y])
        else:
            game_screen.blit(scoreboard_no_sword_images[sword_part_num], [sword_x + sword_part_num * sword_gap, icon_y])



def intro():

    game_screen.blit(intro_screen, [0, 0])


    level = 0
    while level < 1 or level > 2:
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_1]:
                level = 1
            elif key_pressed[pygame.K_2]:
                level = 2

            pygame.display.update()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    return level



if __name__ == '__main__':
    pygame.init()
    game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Snake Heart')

    intro_screen = pygame.image.load("intro_screen.png").convert()
    game_over_win_image = pygame.image.load("game_over_win.png").convert()
    game_over_lose_image = pygame.image.load("game_over_lose.png").convert()

    scoreboard_image = pygame.image.load("scoreboard.png").convert()
    scoreboard_heart_image = pygame.image.load("scoreboard_heart.png").convert()
    scoreboard_no_heart_image = pygame.image.load("scoreboard_no_heart.png").convert()
    scoreboard_spade_image = pygame.image.load("scoreboard_spade.png").convert()
    scoreboard_no_spade_image = pygame.image.load("scoreboard_no_spade.png").convert()

    scoreboard_sword_images = []
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_1.png").convert())
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_2.png").convert())
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_3.png").convert())
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_4.png").convert())

    scoreboard_no_sword_images = []
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_1.png").convert())
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_2.png").convert())
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_3.png").convert())
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_4.png").convert())

    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_4.png").convert())

    pygame.key.set_repeat(10, 20)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 16)

    main()