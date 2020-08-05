
##############################################################
#                  MASTER FILE FOR THIS CODE
# ***UPDATES:
#           + Added a button feature and refurbished Classes
#           + A change in Font types and sizes
#           + Refurbished functions features
#           + Bug fixes
#
# Credits could be seen in the engine file. [engine.py]
##############################################################

import pygame
import sys
import time

from engine import q, listen
from settings import Settings
from threading import Thread

# set the FPS for game play
FPS = 45
fpClock = pygame.time.Clock()

def text_obj(text, font): # to render the text using pygame.font
    pygame.font.init()
    text_surface = font.render(text, True, (0,0,0))
    return text_surface, text_surface.get_rect()

def button(msg, x, y, w, h, ic, ac, screen): # button for the title/header
    game_settings = Settings()
    mouse = pygame.mouse.get_pos() # get a mouse's position
    click = pygame.mouse.get_pressed() # to make the mouse click-able
    pygame.draw.rect(screen, ic, (x, y, w, h))
    textSurf, textRect = text_obj(msg, game_settings.titleFont3)
    textRect.center = (w / 2, y + h / 2)
    if x + w > mouse[0] and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1:
            run_game()
        else:
            pygame.draw.rect(screen, ac,(x, y, w, h))

    # puts the location of the text
    screen.blit(textSurf, textRect) # blit it!

def title():

    pygame.init()
    game_settings = Settings()
    pygame.display.set_caption("Pitch Checker")
    game_icon = pygame.image.load("music.png")
    pygame.display.set_icon(game_icon)
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    screen.fill(game_settings.bg_color)

    while True:
        screen.fill(game_settings.bg_color)
        #time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        button("START LISTENING!", game_settings.buttonx, game_settings.buttony, game_settings.button_width, game_settings.button_height, (255, 255, 0),(90, 255, 0), screen)
        pygame.display.update() # updates the screen

def run_game():

    game_settings = Settings()
    pygame.display.set_caption("Pitch Checker")
    game_icon = pygame.image.load("music.png")
    pygame.display.set_icon(game_icon)
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    screen.fill(game_settings.bg_color)
    pygame.mouse.set_visible(False)

    # headers and title
    title = game_settings.titleFont.render("Sing a", True, game_settings.green1)
    current_title = game_settings.titleFont2.render("Low Note !", True, game_settings.yellow)
    save_title = game_settings.titleFont.render("", True, game_settings.white)

    # runs a background task to the thread and exits when the game is closed
    t = Thread(target = listen)
    t.daemon = True
    t.start()

    # initializing
    low_note = ""
    high_note = ""
    have_low = False
    have_high = False

    hold_length = 10  # how many samples in a row the user needs to hold a note
    existing_note = 1  # keep track of how long current note is held
    current_note = ""  # string of the current note

    tolerance = 155  # how much deviance from proper note to tolerate...

    # MAIN LOOP
    while True:
        screen.fill(game_settings.bg_color)
        #time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        # draw lines to show visually how far away from note voice is
        game_settings.draw(screen)

        # the user SHOULD BE SINGING if there's a note on the queue!
        # CENTS are used to measure in between half steps
        # using CENTS we can tell how far away a note is from the “perfect pitch” (ideal sound for our note)
        if not q.empty():
            b = q.get()
            # accurate notes
            if b["Cents"] < tolerance:
                pygame.draw.circle(screen, game_settings.green, (game_settings.screen_width // 2 + (int(b["Cents"]) * 2), 300), 7)
            # inaccurate notes
            else:
                pygame.draw.circle(screen, game_settings.red, (game_settings.screen_width // 2 + (int(b["Cents"]) * 2), 300), 7)

            # displaying the note
            music_note = game_settings.noteFont.render(b["Note"], True, game_settings.green1)

            # hold your note..!
            if b["Note"] == existing_note:
                current_note += 1

                if current_note == hold_length:

                    # low note obtained..!
                    if not have_low:
                        low_note = existing_note
                        have_low = True
                        current_title = game_settings.titleFont.render("High Note !", True, game_settings.green3)

                    # to check whether the high note is NOT lower than the low note
                    else:
                        if int(existing_note[-1]) <= int(low_note[-1]):
                            current_note = 0  # repeat it again..

                        # finish..!
                        elif int(existing_note[-1]) and not high_note:
                            high_note = existing_note
                            have_high = True
                            title = game_settings.titleFont.render("Perfect!", True, game_settings.white)
                            current_title = game_settings.noteFont.render(str(low_note) + " to " + str(high_note), True, game_settings.green)

                            # saving the result
                            temp = ""
                            file = open("result.txt", "a+")
                            temp = (str(low_note) + " to " + str(high_note) + "\n----------------\n")
                            file.write(temp)
                            file.close()
                            time.sleep(1.5)

                            save_title = game_settings.titleFont.render("SAVED!", True, game_settings.white)
                            pygame.mouse.set_visible(True)
                            #title()
            # if your voice is not accurate yet...
            else:
                existing_note = b["Note"]
                current_note = 1

            screen.blit(music_note, (50, 400)) # placing the music note
        # placing the headers
        screen.blit(title, (10,  80))
        screen.blit(current_title, (10, 120))
        screen.blit(save_title, (10, 200))

        pygame.display.flip()

fpClock.tick(FPS)
title()
run_game()