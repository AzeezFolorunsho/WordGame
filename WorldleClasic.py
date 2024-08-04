import pygame
import sys
import random
from words import *
from Funtions.text import *
from Funtions.textbox_grid import *
from Funtions.textbox import *
from Funtions.indication import *
from Funtions.on_screen_keyboard import *
from Funtions.game_results import *

from Funtions import *
from Funtions.guides import *


# initiates pygame session allowing pygame functions to be used .
pygame.init()

# 1). CONSTANTS:

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ICON = pygame.image.load("assets/wordle+logo.png")
pygame.display.set_icon(ICON)
pygame.display.set_caption("Wordle+ Clasic")

#   a). COLORS
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#787c7e"
LIGHT_GREY = "#d3d6da"
MEDIUM_GREY = "#878a8c"
GREEN = "#6aaa64"
YELLOW = "#c9b458"
RED = "#FF0000"

BACKGROUND_COLOR = WHITE

# fill the screen with a color to wipe away anything from last frame
SCREEN.fill(BACKGROUND_COLOR)

#       the correct word, that is being guessed
CORRECT_WORD = "coder" # tempraraly "coder" for testing purposes, change to random.choice(WORDS)

#   b). FONT

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
ON_SCREEN_KEYBOARD_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
GAME_RESULTS_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)

#       a list of letters in the alphabet
ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"

#   c). TEXTBOX:

#       Calculate the starting position of the textbox_grid and textbox`es
TEXTBOX_START_X = 468
#       *IGNORE* a calculated x position: (SCREEN_WIDTH - ((square_size * word_length) + (TEXTBOX_X_SPACING * (word_length - 1)))) / 2
TEXTBOX_START_Y = 3.6
#       *IGNORE* a calculated y postion: (SCREEN_HEIGHT - ((square_size * max_guesses) + (TEXTBOX_Y_SPACING * (max_guesses - 1)))) / (max_guesses + square_size)

#       textbox spacing
TEXTBOX_X_SPACING = 8
TEXTBOX_Y_SPACING = 20

#        Calculate the size of each square.
TEXTBOX_SIZE = 62.4

#   d). ON SCREEN KEYBOARD:

#       Calculate the starting position of the on screen keyboard
ON_SCREEN_KEYBOARD_START_X = SCREEN_WIDTH / 3.3
ON_SCREEN_KEYBOARD_START_Y = SCREEN_HEIGHT / 1.47

#       Calculate the spacing between each button
ON_SCREEN_KEYBOARD_X_SPACING = 10
ON_SCREEN_KEYBOARD_Y_SPACING = 20

#       Calculate the size of each button
ON_SCREEN_KEYBOARD_WIDTH = TEXTBOX_SIZE / 1.5 #42
ON_SCREEN_KEYBOARD_HEIGHT = TEXTBOX_SIZE #62

# 2) Global Variables (that will be used throughout the program)

#   keeps track of where the next letter will be drawn
current_textbox_x = TEXTBOX_START_X
current_textbox_y = TEXTBOX_START_Y

#   word_length is the number of letters in the correct word.
correct_word_length = len(CORRECT_WORD)

#   guesses_count is used to keep track of how many guesses have been made
guesses_count = 0

#   max_guesses is the maximum number of guesses that can be made.
max_guesses = 6

#   guesses is a 2D list that will store guesses. A guess will be a list of textboxe objects.
#   The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[]] * max_guesses

#   current_guess is a list that will store the letters that have been curently guessed, current_guess_string is a string that will do the same.
current_guess = []
current_guess_string = ""

# determins whether or not the color indicaions should be drawn
indicate = True

# game_result is used to keep track of if the game has been won or not.
game_result = ""

#3.) GAME OBJECTS

# temporary guides for checking alingment.
guides_obj = Guide(SCREEN)
guides_obj.draw_guides_cross(BLACK)
guides_obj.draw_guides_thirds(RED)

# TEXTBOX_GRID (draws the empty grid based on the number of guesses and the length of the word)
textbox_grid_obj = Textbox_grid(TEXTBOX_SIZE, max_guesses, correct_word_length, TEXTBOX_X_SPACING, TEXTBOX_Y_SPACING, TEXTBOX_START_X, TEXTBOX_START_Y, LIGHT_GREY, WHITE)
textbox_grid_obj.draw_grid(SCREEN)

# ONSCREEN_KEYBOARD (draws the on screen keyboard)
on_screen_keyboard_obj = On_Screen_Keyboard(ON_SCREEN_KEYBOARD_START_X, ON_SCREEN_KEYBOARD_START_Y, ON_SCREEN_KEYBOARD_X_SPACING, ON_SCREEN_KEYBOARD_Y_SPACING, ON_SCREEN_KEYBOARD_WIDTH, ON_SCREEN_KEYBOARD_HEIGHT, ON_SCREEN_KEYBOARD_FONT, WHITE, LIGHT_GREY)
    
# GAME RESULTS (draws the game results)
score = 100 # temporary random score

# game_results_obj = Game_Results(0, 0, GAME_RESULTS_FONT, BLACK, WHITE, "Game Results: ", str(score), "Press ENTER to Play Again!", CORRECT_WORD)

# GAME FUNCTIONS

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    # updates the indicators as well, and if all letters are green, the game is won.
    global current_guess, current_guess_string, guesses_count, current_textbox_x, game_result, on_screen_keyboard_obj
    color_chagnging = Indication(on_screen_keyboard_obj, guesses)
    game_decided = False

    for i in range(len(guess_to_check)):
        lowercase_letter = guess_to_check[i].text.lower()
        
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                if indicate == True:
                    color_chagnging.update_bg_color(lowercase_letter, GREEN)
  
                if not game_decided:
                    game_result = "W"

            else:
                if indicate == True:
                    color_chagnging.update_bg_color(lowercase_letter, YELLOW)
                game_result = ""
                game_decided = True

        else:
            if indicate == True:
                color_chagnging.update_bg_color(lowercase_letter, GREY)
            game_result = ""
            game_decided = True
        
        pygame.display.update()
    
    # incraments the number of guesses and resets the current guess for the next guess.
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_textbox_x = TEXTBOX_START_X

    # Checks if your out of guesses and havent guessed the correct word and end game.
    if guesses_count == max_guesses and game_result == "":
        game_result = "L"

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result, textbox_grid_obj, on_screen_keyboard_obj
    SCREEN.fill(BACKGROUND_COLOR)
    guesses_count = 0
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[]] * max_guesses
    current_guess = []
    current_guess_string = ""
    game_result = ""

    textbox_grid_obj.draw_grid(SCREEN)
    for letters in ALPHABET:
        on_screen_keyboard_obj.update_bg_color(letters, LIGHT_GREY)

    pygame.display.update()

def create_new_letter(letter):
    # Creates a new letter and adds it to the current guess.
    global current_guess_string, current_textbox_x, current_textbox_y, guesses_count

    current_guess_string += letter
    current_textbox_y = TEXTBOX_START_Y + guesses_count * (TEXTBOX_SIZE + TEXTBOX_Y_SPACING)    
    new_letter = Textbox(letter, GUESSED_LETTER_FONT, TEXTBOX_SIZE, BLACK, WHITE, LIGHT_GREY, current_textbox_x, current_textbox_y, SCREEN)
    current_textbox_x = TEXTBOX_START_X + len(current_guess_string) * (TEXTBOX_SIZE + TEXTBOX_X_SPACING)    

    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_textbox_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()

    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_textbox_x = TEXTBOX_START_X + len(current_guess_string) * (TEXTBOX_SIZE + TEXTBOX_X_SPACING)
    

# Game Loop
while True:

    # on_screen_keyboard events
    for keys in on_screen_keyboard_obj.key_button_list:
        button_clicked = keys.draw(SCREEN)
        
        if button_clicked == "ENT":
            if game_result != "":
                reset()
            else:
                if len(current_guess_string) == correct_word_length and current_guess_string.lower() in WORDS:
                    check_guess(current_guess)
        elif button_clicked == "DEL":
            if len(current_guess_string) > 0:
                delete_letter()
        else:
            if str(button_clicked) in ALPHABET:
                letter_pressed = button_clicked.upper()

                if len(current_guess_string) < correct_word_length:
                    create_new_letter(letter_pressed)

    # keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) == correct_word_length and current_guess_string.lower() in WORDS:
                        check_guess(current_guess)
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in ALPHABET and key_pressed != "":
                    if len(current_guess_string) < correct_word_length:
                        create_new_letter(key_pressed)
    
    if game_result != "":
        # play_again()
        if game_result == "W":
            game_results_obj = Game_Results(0, 0, GAME_RESULTS_FONT, BLACK, WHITE, "You won! =^)", str(score), "Press ENTER to Play Again!", CORRECT_WORD)
        else:
            game_results_obj = Game_Results(0, 0, GAME_RESULTS_FONT, BLACK, WHITE, "You Lost! =^(", str(score), "Press ENTER to Play Again!", CORRECT_WORD)
        
        game_results_obj.draw_results(SCREEN)
    
    # flip() the display to put your work on screen
    pygame.display.flip()
