import pygame
import screen
import csv
import random
import player_class

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



        self.screen_cols = int(screen.SCREENWIDTH / screen.TILE_SIZE)
        self.screen_rows = int(screen.SCREENHEIGHT / screen.TILE_SIZE)

        self.map_tile_x = 0
        self.map_tile_y = 0
        self.map_tile_step_x = 0
        self.map_tile_step_y = 0

        self.player_row = int(screen.SCREENHEIGHT / screen.TILE_SIZE/ 2 + 1)
        self.player_col_left = int(screen.SCREENWIDTH / screen.TILE_SIZE / 2)
        self.player_col_right = int(screen.SCREENWIDTH / screen.TILE_SIZE / 2 + 1)

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
                self.dx = player_class.PLAYER_MOVE
                self.dy = 0
        elif direction == 'left':
            if self.map_tile_x < self.map_cols - self.screen_cols - 1:
                #self.map_tile_step_x -= PLAYER_MOVE
                self.dx = -player_class.PLAYER_MOVE
                self.dy = 0
        elif direction == 'down':
            if self.map_tile_y > 0:
                #self.map_tile_step_y += PLAYER_MOVE
                self.dx = 0
                self.dy = player_class.PLAYER_MOVE
        elif direction == 'up':
            if self.map_tile_y < self.map_rows - self.screen_rows - 1:
                #self.map_tile_step_y -= PLAYER_MOVE
                self.dx = 0
                self.dy = -player_class.PLAYER_MOVE

        self.map_tile_step_x += self.dx
        self.map_tile_step_y += self.dy



        if self.map_tile_step_x >= screen.TILE_SIZE:
            self.map_tile_step_x -= screen.TILE_SIZE
            self.map_tile_x -= 1

        if self.map_tile_step_x < 0:
            self.map_tile_step_x += screen.TILE_SIZE
            self.map_tile_x += 1

        if self.map_tile_step_y >= screen.TILE_SIZE:
            self.map_tile_step_y -= screen.TILE_SIZE
            self.map_tile_y -= 1

        if self.map_tile_step_y < 0:
            self.map_tile_step_y += screen.TILE_SIZE
            self.map_tile_y += 1

    def draw(self, display):
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

                #game_screen.blit(display_image, [(col - 1) * TILE_SIZE + self.map_tile_step_x,
                #                                (row - 1) * TILE_SIZE + self.map_tile_step_y])

                display.show_image(display_image, (col - 1) * screen.TILE_SIZE + self.map_tile_step_x, (row - 1) * screen.TILE_SIZE + self.map_tile_step_y)

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
        if (tile_left == item and self.map_tile_step_x > player_class.PLAYER_MOVE) or tile_right == item:
            player_touching_item = True

        return player_touching_item

    def remove_item(self, item, tile_left, tile_right):
        if (tile_left == item and self.map_tile_step_x > player_class.PLAYER_MOVE):
            self.tile_list[self.player_row + self.map_tile_y + 1][self.player_col_left + self.map_tile_x] = 'l'
        elif tile_right == item:
            self.tile_list[self.player_row + self.map_tile_y + 1][self.player_col_right+ self.map_tile_x] = 'l'