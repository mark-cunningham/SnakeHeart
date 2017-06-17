import pygame

SCREENWIDTH = 640
SCREENHEIGHT = 480
TILE_SIZE = 16

class Display(object):
    def __init__(self):
        self.game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Snake Heart')

        self.intro_screen = pygame.image.load("intro_screen.png").convert()
        self.game_over_win_image = pygame.image.load("game_over_win.png").convert()
        self.game_over_lose_image = pygame.image.load("game_over_lose.png").convert()

        self.scoreboard_image = pygame.image.load("scoreboard.png").convert()
        self.scoreboard_heart_image = pygame.image.load("scoreboard_heart.png").convert()
        self.scoreboard_no_heart_image = pygame.image.load("scoreboard_no_heart.png").convert()
        self.scoreboard_spade_image = pygame.image.load("scoreboard_spade.png").convert()
        self.scoreboard_no_spade_image = pygame.image.load("scoreboard_no_spade.png").convert()

        self.scoreboard_sword_images = []
        self.scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_1.png").convert())
        self.scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_2.png").convert())
        self.scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_3.png").convert())
        self.scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_4.png").convert())

        self.scoreboard_no_sword_images = []
        self.scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_1.png").convert())
        self.scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_2.png").convert())
        self.scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_3.png").convert())
        self.scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_4.png").convert())

    def show_image(self, image, x, y):
        self.game_screen.blit(image, [x, y])