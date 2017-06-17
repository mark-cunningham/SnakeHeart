import pygame
import screen
import random



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

        self.rect.x = (start_tile_col - map.map_tile_x) * screen.TILE_SIZE
        self.rect.y = (start_tile_row - map.map_tile_y) * screen.TILE_SIZE






    def draw(self, display):
        if self.alive is True:
            #game_screen.blit(self.monster_image, [self.rect.x, self.rect.y])
            display.show_image(self.monster_image, self.rect.x, self.rect.y)

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
        monster_tile_x_1 = int(self.rect.x / screen.TILE_SIZE) + 1
        monster_tile_x_2 = int((self.rect.x + self.rect.width) / screen.TILE_SIZE) + 1
        monster_tile_y_1 = int(self.rect.y / screen.TILE_SIZE) + 1
        monster_tile_y_2 = int((self.rect.y + self.rect.height) / screen.TILE_SIZE) + 1



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
        self.rect.x += portal_x * screen.TILE_SIZE
        self.rect.y += portal_y * screen.TILE_SIZE


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