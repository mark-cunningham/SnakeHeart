# Snake Heart
# © Code Angel 2017

import pygame, sys
from pygame.locals import *

import screen
import player_class
import monster_class
import map_class


# Define the colours
WHITE = (255, 255, 255)
GREEN = (51, 223, 32)

def main():

    player = player_class.Player()
    map = map_class.Map()

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
        bumbler = monster_class.Bumbler(map.level)
        bumbler.spawn_location(map)
        bumblers.append(bumbler)

    for whizzer_count in range(whizzers_spawn_start):
        whizzer = monster_class.Whizzer(map.level)
        whizzer.spawn_location(map)
        whizzers.append(whizzer)

    for boxer_count in range(boxers_spawn_start):
        boxer = monster_class.Boxer(map.level)
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

        map.draw(display)
        player.draw(display)

        for bumbler in bumblers:
            bumbler.draw(display)

        for whizzer in whizzers:
            whizzer.draw(display)

        for boxer in boxers:
            boxer.draw(display)


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

            monster_class.Bumbler.spawn(bumblers, map)
            monster_class.Whizzer.spawn(whizzers, map)
            monster_class.Boxer.spawn(boxers, map)


        display_scoreboard(player.gold, player.lives, player.spades, player.sword)

        if player.game_over_lose is True:
            #game_screen.blit(game_over_lose_image, [110, 380])
            display.show_image(display.game_over_lose_image, 110, 380)

        if player.game_over_win is True:
            #game_screen.blit(game_over_win_image, [50, 380])
            display.show_image(display.game_over_win_image, 50, 380)


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
    #game_screen.blit(scoreboard_image, [0, 0])
    display.show_image(display.scoreboard_image, 0, 0)
    #game_screen.blit(map.gold_image, [scoreboard_margin, scoreboard_margin])

    text = font.render(str(gold), True, WHITE)
    #game_screen.blit(text, [gold_text_x, text_y])
    display.show_image(text, gold_text_x, text_y)

    total_kills = monster_class.Bumbler.kills + monster_class.Whizzer.kills + monster_class.Boxer.kills
    text = font.render(str(total_kills), True, WHITE)
    #game_screen.blit(text, [kills_text_x, text_y])
    display.show_image(text, gold_text_x, text_y)

    total_score = gold * gold_score + monster_class.Bumbler.kills * bumbler_score + monster_class.Whizzer.kills * whizzer_score + monster_class.Boxer.kills * boxer_score
    text = font.render(str(total_score), True, GREEN)
    #game_screen.blit(text, [score_text_x, text_y])
    display.show_image(text, score_text_x, text_y)

    for heart in range(lives):
        #game_screen.blit(scoreboard_heart_image, [hearts_x + heart * icon_gap, icon_y])
        display.show_image(display.scoreboard_heart_image, hearts_x + heart * icon_gap, icon_y)

    for no_heart in range(lives, player_class.Player.max_lives):
        #game_screen.blit(scoreboard_no_heart_image, [hearts_x + no_heart * icon_gap, icon_y])
        display.show_image(display.scoreboard_no_heart_image, hearts_x + no_heart * icon_gap, icon_y)

    for spade in range(spades):
        #game_screen.blit(scoreboard_spade_image, [spades_x + spade * icon_gap, icon_y])
        display.show_image(display.scoreboard_spade_image, spades_x + spade * icon_gap, icon_y)

    for no_spade in range(spades, player_class.Player.max_spades):
        #game_screen.blit(scoreboard_no_spade_image, [spades_x + no_spade * icon_gap, icon_y])
        display.show_image(display.scoreboard_no_spade_image, spades_x + no_spade * icon_gap, icon_y)

    for sword_part_num, sword_part in enumerate(sword):
        if sword_part is True:
            #game_screen.blit(scoreboard_sword_images[sword_part_num], [sword_x + sword_part_num * sword_gap, icon_y])
            display.show_image(display.scoreboard_sword_images[sword_part_num], sword_x + sword_part_num * sword_gap, icon_y)
        else:
            display.show_image(display.scoreboard_no_sword_images[sword_part_num], sword_x + sword_part_num * sword_gap, icon_y)
            #game_screen.blit(scoreboard_no_sword_images[sword_part_num], [sword_x + sword_part_num * sword_gap, icon_y])



def intro():

    #game_screen.blit(intro_screen, [0, 0])
    display.show_image(display.intro_screen, 0, 0)


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
    display = screen.Display()
    #game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    #pygame.display.set_caption('Snake Heart')

    #intro_screen = pygame.image.load("intro_screen.png").convert()
    #game_over_win_image = pygame.image.load("game_over_win.png").convert()
    #game_over_lose_image = pygame.image.load("game_over_lose.png").convert()

    """scoreboard_image = pygame.image.load("scoreboard.png").convert()
    scoreboard_heart_image = pygame.image.load("scoreboard_heart.png").convert()
    scoreboard_no_heart_image = pygame.image.load("scoreboard_no_heart.png").convert()
    scoreboard_spade_image = pygame.image.load("scoreboard_spade.png").convert()
    scoreboard_no_spade_image = pygame.image.load("scoreboard_no_spade.png").convert()"""

    """scoreboard_sword_images = []
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_1.png").convert())
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_2.png").convert())
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_3.png").convert())
    scoreboard_sword_images.append(pygame.image.load("scoreboard_sword_4.png").convert())"""

    """scoreboard_no_sword_images = []
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_1.png").convert())
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_2.png").convert())
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_3.png").convert())
    scoreboard_no_sword_images.append(pygame.image.load("scoreboard_no_sword_4.png").convert())"""



    pygame.key.set_repeat(10, 20)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 16)

    main()