# Snake Heart
# © Code Angel 2017

import pygame, sys
from pygame.locals import *
import random
import csv

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
TILE_SIZE = 16

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_MOVE = 4
MONSTER_MOVE = 2


# Player class
class Player(object):

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

        self.image_num = 0

        self.image = self.player_down_image
        self.rect = self.image.get_rect()

        self.reset()

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
        else:
            self.image = self.player_down_image

        if self.image_num >= len(self.player_up_images):
            self.image_num = 0

        game_screen.blit(self.image, [self.rect.x, self.rect.y])


    def reset(self):
        self.set_location([SCREENWIDTH / 2, SCREENHEIGHT / 2])
        self.set_direction('down')
        self.score = 0

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

    def map_sea(self):
        print('dead')

    def map_gold(self):
        self.score += 1
        print(str(self.score))

    def check_collision(self, monster):
        if self.rect.colliderect(monster.rect):
            print('collision')



# Map class
class Map(object):

    def __init__(self):
        self.sea_image = pygame.image.load("sea.png").convert()
        self.land_image = pygame.image.load("land.png").convert()
        self.path_image = pygame.image.load("path.png").convert()
        self.beach_image = pygame.image.load("beach.png").convert()
        self.gold_image = pygame.image.load("gold.png").convert()

        self.map_key = {'s': 'sea',
                   'l': 'land',
                   'p': 'path',
                   'b': 'beach',
                   'g': 'gold'}

        with open('snakeheart map.csv', 'r') as csvfile:
            read_map = csv.reader(csvfile)
            self.tile_list = list(read_map)

        self.map_cols = len(self.tile_list[0])
        self.map_rows = len(self.tile_list)

        self.screen_cols = SCREENWIDTH / TILE_SIZE
        self.screen_rows = SCREENHEIGHT / TILE_SIZE

        self.map_tile_x = 0
        self.map_tile_y = 0
        self.map_tile_step_x = 0
        self.map_tile_step_y = 0

        self.player_row = int(SCREENHEIGHT / TILE_SIZE/ 2 + 2)
        self.player_col_left = int(SCREENWIDTH / TILE_SIZE / 2)
        self.player_col_right = int(SCREENWIDTH / TILE_SIZE / 2 + 1)

        self.dx = 0
        self.dy = 0


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
        for row in range(31):
            for col in range(41):
                tile = self.map_key.get(self.tile_list[row + self.map_tile_y][col + self.map_tile_x])
                display_image = ''
                if tile == 'sea':
                    display_image = self.sea_image
                elif tile == 'land':
                    display_image = self.land_image
                elif tile == 'path':
                    display_image = self.path_image
                elif tile == 'gold':
                    display_image = self.gold_image
                elif tile == 'beach':
                    display_image = self.beach_image

                game_screen.blit(display_image, [(col - 1) * TILE_SIZE + self.map_tile_step_x,
                                                 (row - 1) * TILE_SIZE + self.map_tile_step_y])
    def reset_change(self):
        self.dx = 0
        self.dy = 0

    def check_player_loc(self, player):
        tile_left = self.map_key.get(self.tile_list[self.player_row + self.map_tile_y][self.player_col_left + self.map_tile_x])
        tile_right = self.map_key.get(self.tile_list[self.player_row + self.map_tile_y][self.player_col_right + self.map_tile_x])

        touching_sea = self.player_touching('sea', tile_left, tile_right)
        touching_gold = self.player_touching('gold', tile_left, tile_right)

        if touching_sea:
            player.map_sea()
        elif touching_gold:
            player.map_gold()
            self.remove_item('gold', tile_left, tile_right)






    def player_touching(self, item, tile_left, tile_right):
        player_touching_item = False
        if (tile_left == item and self.map_tile_step_x > PLAYER_MOVE) or tile_right == item:
            player_touching_item = True

        return player_touching_item

    def remove_item(self, item, tile_left, tile_right):
        if (tile_left == item and self.map_tile_step_x > PLAYER_MOVE):
            self.tile_list[self.player_row + self.map_tile_y][self.player_col_left + self.map_tile_x] = 'l'
        elif tile_right == item:
            self.tile_list[self.player_row + self.map_tile_y][self.player_col_right+ self.map_tile_x] = 'l'



class Monster():
    def __init__(self):
        self.monster_image = pygame.image.load("monster_down.png").convert()
        self.rect = self.monster_image.get_rect()
        self.direction = 'right'

        self.random_direction = 20
        self.intelligence = 5

    def spawn_location(self, map):

        start_tile_col = random.randint(0, map.map_cols - 1)
        start_tile_row = random.randint(0, map.map_rows - 1)

        terrain = map.map_key.get(map.tile_list[start_tile_row][start_tile_col])
        while terrain != 'land':
            start_tile_col = random.randint(0, map.map_cols - 1)
            start_tile_row = random.randint(0, map.map_rows - 1)

            terrain = map.map_key.get(map.tile_list[start_tile_row][start_tile_col])

        self.rect.x = start_tile_col * TILE_SIZE
        self.rect.y = start_tile_row * TILE_SIZE




    def draw(self):
        game_screen.blit(self.monster_image, [self.rect.x, self.rect.y])

    def move(self, map):
        if self.direction == 'right':
            self.rect.x += MONSTER_MOVE
        elif self.direction == 'left':
            self.rect.x -= MONSTER_MOVE
        elif self.direction == 'down':
            self.rect.y += MONSTER_MOVE
        elif self.direction == 'up':
            self.rect.y -= MONSTER_MOVE


        self.rect.x += map.dx
        self.rect.y += map.dy

        self.check_terrain(map)






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

    def check_terrain(self, map):
        self.monster_tile_x = int(self.rect.x / TILE_SIZE)
        self.monster_tile_y = int(self.rect.y / TILE_SIZE)
        terrain_type = map.map_key.get(map.tile_list[map.map_tile_y + self.monster_tile_y][map.map_tile_x + self.monster_tile_x])
        if terrain_type == 'beach':
            if self.direction == 'up':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'up'
            elif self.direction == 'right':
                self.direction = 'left'
            elif self.direction == 'left':
                self.direction = 'right'

        elif terrain_type == 'path':
            self.monster_image = map.beach_image

        else:
            self.maybe_change_direction()




def main():

    player = Player()
    map = Map()
    monster_1 = Monster()
    monster_2 = Monster()
    monster_3 = Monster()
    monster_1.spawn_location(map)
    monster_2.spawn_location(map)
    monster_3.spawn_location(map)

    while True:  # main game loop
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

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


            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        monster_1.move(map)
        monster_2.move(map)
        monster_3.move(map)
        map.reset_change()

        map.draw()
        player.draw()

        monster_1.draw()
        monster_2.draw()
        monster_3.draw()

        map.check_player_loc(player)

        player.check_collision(monster_1)



        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Snake Heart')
    pygame.key.set_repeat(10, 20)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 16)

    main()