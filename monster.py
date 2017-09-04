# Toadie
# Code Angel

# Classes: Monster, Bumber, Whizzer and Boxer

import utils

import screen
import random


class Monster:

    def __init__(self, image, speed):

        self.monster_image = utils.load_media('image', image)

        self.rect = self.monster_image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.speed = speed

        self.direction = None

        self.alive = True

        # The terrain types at either side of the monster
        self.terrain_type_1 = None
        self.terrain_type_2 = None
        self.terrain_type_3 = None
        self.terrain_type_4 = None

    def standard_direction(self):
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def diagonal_direction(self):
        self.direction = random.choice(['up right', 'down right', 'down left', 'up left'])

    # Calculate a random spawn location which must be on land
    def spawn_location(self, game_map):

        start_tile_col = random.randint(0, game_map.map_cols - 1)
        start_tile_row = random.randint(0, game_map.map_rows - 1)

        terrain = game_map.map_key.get(game_map.tile_list[start_tile_row][start_tile_col])
        while terrain != 'land':
            start_tile_col = random.randint(0, game_map.map_cols - 1)
            start_tile_row = random.randint(0, game_map.map_rows - 1)

            terrain = game_map.map_key.get(game_map.tile_list[start_tile_row][start_tile_col])

        self.rect.x = (start_tile_col - game_map.map_tile_x) * screen.TILE_SIZE
        self.rect.y = (start_tile_row - game_map.map_tile_y) * screen.TILE_SIZE

    # Draw the monster passing the image and location to the Display class
    def draw(self, display):
        if self.alive is True:
            display.show_image(self.monster_image, self.rect.x, self.rect.y)

    # Move the monster
    def move(self, game_map):

        if self.alive is True:

            # Update the x and y location based on the direction the monster is moving in
            if 'right' in self.direction:
                self.rect.x += self.speed
            if 'left' in self.direction:
                self.rect.x -= self.speed
            if 'down' in self.direction:
                self.rect.y += self.speed
            if 'up' in self.direction:
                self.rect.y -= self.speed

            # Update the monster's location based on any map scrolling
            self.rect.x += game_map.dx
            self.rect.y += game_map.dy

            # Update the surrounding terrain details, check if fallen into hole / drowned, and maybe change direction
            self.update_surrounding_terrain(game_map)
            self.check_for_hole()
            self.check_if_drowned()
            self.maybe_change_direction()

    # The tiles surrounding the monster
    # Used because the map scrolls by less than a full tile size
    def update_surrounding_terrain(self, game_map):
        monster_tile_x_1 = int(self.rect.x / screen.TILE_SIZE) + 1
        monster_tile_x_2 = int((self.rect.x + self.rect.width) / screen.TILE_SIZE) + 1
        monster_tile_y_1 = int(self.rect.y / screen.TILE_SIZE) + 1
        monster_tile_y_2 = int((self.rect.y + self.rect.height) / screen.TILE_SIZE) + 1

        # Work out what is actually in the terrain surrounding the monster
        rel_y1 = game_map.map_tile_y + monster_tile_y_1
        rel_x1 = game_map.map_tile_x + monster_tile_x_1
        rel_y2 = game_map.map_tile_y + monster_tile_y_2
        rel_x2 = game_map.map_tile_x + monster_tile_x_2
        self.terrain_type_1 = game_map.map_key.get(game_map.tile_list[rel_y1][rel_x1])
        self.terrain_type_2 = game_map.map_key.get(game_map.tile_list[rel_y1][rel_x2])
        self.terrain_type_3 = game_map.map_key.get(game_map.tile_list[rel_y2][rel_x1])
        self.terrain_type_4 = game_map.map_key.get(game_map.tile_list[rel_y2][rel_x2])

    # Test if the monster fallen into a hole
    def check_for_hole(self):

        if self.alive is True:

            if (self.terrain_type_1 == 'trap' or
                    self.terrain_type_2 == 'trap' or
                    self.terrain_type_3 == 'trap' or
                    self.terrain_type_4 == 'trap'):

                # The monster has fallen into a hole, so alive will be false and kills need to be updated
                self.alive = False
                self.update_kills()

    # Overridden in Bumbler, Whizzer and Boxer
    def update_kills(self):
        pass

    # Test if the monster has fallen into water
    def check_if_drowned(self):
        if self.alive is True:
            if (self.terrain_type_1 == 'water' or
                    self.terrain_type_2 == 'water' or
                    self.terrain_type_3 == 'water' or
                    self.terrain_type_4 == 'water'):

                self.alive = False

    # Overridden in Bumbler and Boxer - Whizzer does not change direction
    def maybe_change_direction(self):
        pass

    # The player has used a portal, so the relative postion of the monster will need to change accordingly
    def portal(self, portal_x, portal_y):
        self.rect.x += portal_x * screen.TILE_SIZE
        self.rect.y += portal_y * screen.TILE_SIZE


# Bumbler class inherits from Monster
class Bumbler(Monster):

    # Class variables
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

        super().__init__("monster_down", speed)
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
                if self.rect.y < screen.SCREENHEIGHT / 2:
                    self.direction = 'down'
                else:
                    self.direction = 'up'
            elif smart_change == 2:
                if self.rect.x < screen.SCREENWIDTH / 2:
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

        super().__init__("whizzer_down", speed)
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

        super().__init__("boxer_down", speed)
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