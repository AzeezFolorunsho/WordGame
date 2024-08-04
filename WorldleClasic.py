import pygame
import sys
import random
from words import *
from Funtions.text import *
from Funtions.text_box_grid import *
from Funtions.text_box import *
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

#       fill the screen with a color to wipe away anything from last frame
SCREEN.fill(BACKGROUND_COLOR)

#       the correct word, that is being guessed
CORRECT_WORD = "coder" # tempraraly "coder" for testing purposes, change to random.choice(WORDS)

#   b). FONT

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
ON_SCREEN_KEYBOARD_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
GAME_RESULTS_FONT = pygame.font.Font("assets/FreeSansBold.otf", 40)

#       a list of letters in the alphabet
# ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"

#   c). TEXTBOX SPACING (defines the spacing between letters)
TEXTBOX_X_SPACING = 8
TEXTBOX_Y_SPACING = 20

#   d). TEXTBOX POSITION AND SIZE

#       Calculate the starting position of the grid.
START_X = 468
#       a calculated x position: (SCREEN_WIDTH - ((square_size * word_length) + (TEXTBOX_X_SPACING * (word_length - 1)))) / 2

START_Y = 3.6
#       a calculated y postion: (SCREEN_HEIGHT - ((square_size * max_guesses) + (TEXTBOX_Y_SPACING * (max_guesses - 1)))) / (max_guesses + square_size)

#        Calculate the size of each square.
TEXT_BOX_SIZE = 62.4

# 2) Global Variables (that will be used throughout the program)

#   keeps track of where the next letter will be drawn
current_textbox_x = START_X
current_textbox_y = START_Y

#   word_length is the number of letters in the correct word.
correct_word_length = len(CORRECT_WORD)

#   guesses_count is used to keep track of how many guesses have been made
guesses_count = 0

#   max_guesses is the maximum number of guesses that can be made.
max_guesses = 6

#   guesses is a 2D list that will store guesses. A guess will be a list of text_boxe objects.
#   The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[]] * max_guesses

#   current_guess is a list that will store the letters that have been curently guessed, current_guess_string is a string that will do the same.
current_guess = []
current_guess_string = ""

# determins whether or not the color indicaions should be drawn
indicate = True

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []
on_screen_keyboard_keys = []

# game_result is used to keep track of if the game has been won or not.
game_result = ""

# legacy code for testing purposes (TO BE REMOVED)
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

# Experiment

LETTER_KEYS = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], 
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"], 
        ["Z", "X", "C", "V", "B", "N", "M"]]

#3.) GAME OBJECTS

# TEXT_BOX_GRID (draws the empty grid based on the number of guesses and the length of the word)
guess_grid = Text_box_grid(TEXT_BOX_SIZE, max_guesses, correct_word_length, TEXTBOX_X_SPACING, TEXTBOX_Y_SPACING, START_X, START_Y, LIGHT_GREY, WHITE)

# ONSCREEN_KEYBOARD (draws the on screen keyboard)
on_screen_keyboard = On_Screen_Keyboard(START_X - TEXT_BOX_SIZE, START_Y + (TEXT_BOX_SIZE + TEXTBOX_Y_SPACING) * max_guesses, ON_SCREEN_KEYBOARD_FONT, MEDIUM_GREY)

# GAME FUNCTIONS

def generate_on_screen_keyboard():
    # Generates the on screen keyboard keys
    global on_screen_keyboard_keys
    on_screen_keyboard_keys = []

    

    for row in LETTER_KEYS:
        for key in LETTER_KEYS[row]:
            on_screen_keyboard_keys.append(Text_Button(key, TEXT_BOX_SIZE, LETTER_KEYS.index(row) * (TEXT_BOX_SIZE + TEXTBOX_Y_SPACING), TEXT_BOX_SIZE, TEXT_BOX_SIZE, LIGHT_GREY, WHITE))

class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.text_pos = (self.x + ((TEXT_BOX_SIZE / 1.5) / 2), self.y + (TEXT_BOX_SIZE / 2.5))
        self.rect = (self.x, self.y, TEXT_BOX_SIZE / 1.5, TEXT_BOX_SIZE)
        self.bg_color = LIGHT_GREY

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = ON_SCREEN_KEYBOARD_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center = self.text_pos)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def update(self, letter, color):
        # Updates the color of the indicator according to the guessed letter, and the input color.
        if self.text == letter.upper():
            self.bg_color = color
            self.draw()
    
    @staticmethod
    def draw_indicators():
    # Drawing the indicators on the screen.
        global indicators
        
        indicator_x = START_X - ((TEXT_BOX_SIZE * correct_word_length) - TEXTBOX_X_SPACING )/ correct_word_length
        indicator_y = START_Y + ((TEXT_BOX_SIZE * max_guesses) + (TEXTBOX_Y_SPACING * (max_guesses - 1))) + (TEXTBOX_Y_SPACING / 2)

        for i in range(3):
            for letter in ALPHABET[i]:
                new_indicator = Indicator(indicator_x, indicator_y, letter)
                indicators.append(new_indicator)
                new_indicator.draw()
                indicator_x += TEXT_BOX_SIZE - TEXTBOX_X_SPACING * 2
            indicator_y += TEXT_BOX_SIZE + TEXTBOX_X_SPACING * 2
            if i == 0:
                indicator_x = (START_X - ((TEXT_BOX_SIZE * correct_word_length) - TEXTBOX_X_SPACING )/ correct_word_length) + (new_indicator.rect[2] / 2)
            elif i == 1:
                indicator_x = (START_X - ((TEXT_BOX_SIZE * correct_word_length) - TEXTBOX_X_SPACING )/ correct_word_length) + (new_indicator.rect[2] * 1.6)
Indicator.draw_indicators()

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    # updates the indicators as well, and if all letters are green, the game is won.
    global current_guess, current_guess_string, guesses_count, current_textbox_x, game_result
    color_chagnging = Indication(indicators, guesses)
    game_decided = False

    for i in range(len(guess_to_check)):
        lowercase_letter = guess_to_check[i].text.lower()
        
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                if indicate == True:
                    color_chagnging.update(lowercase_letter, GREEN)
  
                if not game_decided:
                    game_result = "W"

            else:
                if indicate == True:
                    color_chagnging.update(lowercase_letter, YELLOW)
                game_result = ""
                game_decided = True

        else:
            if indicate == True:
                color_chagnging.update(lowercase_letter, GREY)
            game_result = ""
            game_decided = True
        
        pygame.display.update()
    
    # incraments the number of guesses and resets the current guess for the next guess.
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_textbox_x = START_X

    # Checks if your out of guesses and havent guessed the correct word and end game.
    if guesses_count == max_guesses and game_result == "":
        game_result = "L"

def play_again():
    # Puts the play again text on the screen, genarates a box covering indicators.
    pygame.draw.rect(SCREEN, "white", (indicators[0].x, indicators[0].y, ((indicators[9].x - indicators[0].x) + TEXT_BOX_SIZE), ((indicators[-1].y - indicators[0].y) + TEXT_BOX_SIZE)))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT / 1.4))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD.upper()}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT / 1.2))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()
score = 100
results = Game_Results(0, 0, GAME_RESULTS_FONT, BLACK, RED, "You won!", str(score), "Press ENTER to Play Again!", CORRECT_WORD)

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill(BACKGROUND_COLOR)
    guesses_count = 0
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[]] * max_guesses
    current_guess = []
    current_guess_string = ""
    game_result = ""

    guess_grid.draw_grid(SCREEN)
    Indicator.draw_indicators()

    pygame.display.update()

    for indicator in indicators:
        indicator.bg_color = LIGHT_GREY
        indicator.draw()

def create_new_letter(letter):
    # Creates a new letter and adds it to the current guess.
    global current_guess_string, current_textbox_x, current_textbox_y, guesses_count

    current_guess_string += letter
    current_textbox_y = START_Y + guesses_count * (TEXT_BOX_SIZE + TEXTBOX_Y_SPACING)    
    new_letter = Text_box(letter, GUESSED_LETTER_FONT, TEXT_BOX_SIZE, BLACK, WHITE, LIGHT_GREY, current_textbox_x, current_textbox_y, SCREEN)
    current_textbox_x = START_X + len(current_guess_string) * (TEXT_BOX_SIZE + TEXTBOX_X_SPACING)    

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
    current_textbox_x = START_X + len(current_guess_string) * (TEXT_BOX_SIZE + TEXTBOX_X_SPACING)
    
# Game Loop
while True:

    # draw the empty grid based on the number of guesses and the length of the word
    guess_grid.draw_grid(SCREEN)

    # draw the on screen keyboard
    # button_clicked = on_screen_keyboard.draw(SCREEN)
    
    # if button_clicked == "ENT":
    #     if game_result != "":
    #         reset()
    #     else:
    #         if len(current_guess_string) == correct_word_length and current_guess_string.lower() in WORDS:
    #             check_guess(current_guess)
    # elif button_clicked == "DEL":
    #     if len(current_guess_string) > 0:
    #         delete_letter()
    # else:
    #     if button_clicked == "QWERTYUIOPASDFGHJKLZXCVBNM":
    #         letter_pressed = button_clicked.upper()
    #         if len(current_guess_string) < correct_word_length:
    #             create_new_letter(letter_pressed)

    # temporary guides for checking alingment.
    alignment_guides = Guide(SCREEN)
    alignment_guides.draw_guides_cross(BLACK)
    alignment_guides.draw_guides_thirds(RED)

    if game_result != "":
        # play_again()
        results.draw_results(SCREEN)

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
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < correct_word_length:
                        create_new_letter(key_pressed)
    
     # flip() the display to put your work on screen
    pygame.display.flip()
