import pygame
import os

import monster
import player_class

# Define the colours
WHITE = (255, 255, 255)
GREEN = (51, 223, 32)

def display_scoreboard(display, font, gold, lives, spades, sword):
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

    display.show_image(display.scoreboard_image, 0, 0)

    text = font.render(str(gold), True, WHITE)
    display.show_image(text, gold_text_x, text_y)

    total_kills = monster.Bumbler.kills + monster.Whizzer.kills + monster.Boxer.kills
    text = font.render(str(total_kills), True, WHITE)
    display.show_image(text, kills_text_x, text_y)

    total_score = gold * gold_score + monster.Bumbler.kills * bumbler_score + monster.Whizzer.kills * whizzer_score + monster.Boxer.kills * boxer_score
    text = font.render(str(total_score), True, GREEN)
    display.show_image(text, score_text_x, text_y)

    for heart in range(lives):
        display.show_image(display.scoreboard_heart_image, hearts_x + heart * icon_gap, icon_y)

    for no_heart in range(lives, player_class.Player.max_lives):
        display.show_image(display.scoreboard_no_heart_image, hearts_x + no_heart * icon_gap, icon_y)

    for spade in range(spades):
        display.show_image(display.scoreboard_spade_image, spades_x + spade * icon_gap, icon_y)

    for no_spade in range(spades, player_class.Player.max_spades):
        display.show_image(display.scoreboard_no_spade_image, spades_x + no_spade * icon_gap, icon_y)

    for sword_part_num, sword_part in enumerate(sword):
        if sword_part is True:
            display.show_image(display.scoreboard_sword_images[sword_part_num],
                               sword_x + sword_part_num * sword_gap, icon_y)
        else:
            display.show_image(display.scoreboard_no_sword_images[sword_part_num],
                               sword_x + sword_part_num * sword_gap, icon_y)



def intro(display):

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

            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.sys.exit()

    return level


def instructions(display):
    display.show_image(display.instructions_screen, 0, 0)

    instructions_read = False

    while instructions_read is False:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_SPACE]:
                instructions_read = True

            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.sys.exit()

            pygame.display.update()


# Get an image or audio from folder
def load_media(media_type, filename):
    media = None
    full_path = os.path.dirname(os.path.realpath(__file__))

    if media_type == 'image':
        images_path = os.path.join(full_path, 'images')
        full_filename = os.path.join(images_path, filename + '.png')
        media = pygame.image.load(full_filename).convert_alpha()
    elif media_type == 'audio':
        audio_path = os.path.join(full_path, 'audio')
        full_filename = os.path.join(audio_path, filename + '.ogg')
        media = pygame.mixer.Sound(full_filename)

    return media