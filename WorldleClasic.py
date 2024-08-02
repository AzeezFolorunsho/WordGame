import pygame
import sys
import random
from words import *
from Funtions import text_box_grid
from Funtions import text_box
from Funtions import indication
from Funtions import guides


# initiates pygame session allowing pygame functions to be used .
pygame.init()

# CONSTANTS

WIDTH, HEIGHT = 1280, 720

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

ICON = pygame.image.load("assets/wordle+logo.png")
pygame.display.set_icon(ICON)
pygame.display.set_caption("Wordle+ Clasic")

WHITE = "#FFFFFF"
BLACK = "#000000"
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
RED = "#FF0000"

OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
Background_color = WHITE

# tempraraly "coder" for testing purposes, change to random.choice(WORDS).
CORRECT_WORD = "coder"

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)

SCREEN.fill(Background_color)

pygame.display.update()

# defines the spacing between letters.
LETTER_X_SPACING = 8
LETTER_Y_SPACING = 20

# Global Variables

# guesses_count is used to keep track of how many guesses have been made
guesses_count = 0

# max_guesses is the maximum number of guesses that can be made.
max_guesses = 6

# word_length is the number of letters in the correct word.
word_length = 5

# guesses is a 2D list that will store guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[]] * max_guesses

# current_guess is a list that will store the letters that have been curently guessed, current_guess_string is a string that will do the same.
current_guess = []
current_guess_string = ""

# Calculate the size of each square.
square_size = 62.4

# determins whether or not the color indicaions should be drawn
indicate = True

# Calculate the starting position of the grid.
start_x = (WIDTH - ((square_size * word_length) + (LETTER_X_SPACING * (word_length - 1)))) / 2
start_y = (HEIGHT - ((square_size * max_guesses) + (LETTER_Y_SPACING * (max_guesses - 1)))) / (max_guesses + square_size)

# current_letter_bg_x is used to keep track of where the next letter will be drawn.
current_letter_bg_x = start_x
current_letter_bg_y = start_y

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

# game_result is used to keep track of if the game has been won or not.
game_result = ""

# GAME FUNCTIONS

guess_grid = text_box_grid.Text_box_grid(square_size, max_guesses, word_length, LETTER_X_SPACING, LETTER_Y_SPACING, start_x, start_y)
guess_grid.draw_grid(SCREEN)

# temporary guides for checking alingment.
alignment_guides = guides.Guide(SCREEN)
alignment_guides.draw_guides_cross(BLACK)
alignment_guides.draw_guides_thirds(RED)

class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.text_pos = (self.x + ((square_size / 1.5) / 2), self.y + (square_size / 2.5))
        self.rect = (self.x, self.y, square_size / 1.5, square_size)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
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
        
        indicator_x = start_x - ((square_size * word_length) - LETTER_X_SPACING )/ word_length
        indicator_y = start_y + ((square_size * max_guesses) + (LETTER_Y_SPACING * (max_guesses - 1))) + (LETTER_Y_SPACING / 2)

        for i in range(3):
            for letter in ALPHABET[i]:
                new_indicator = Indicator(indicator_x, indicator_y, letter)
                indicators.append(new_indicator)
                new_indicator.draw()
                indicator_x += square_size - LETTER_X_SPACING * 2
            indicator_y += square_size + LETTER_X_SPACING * 2
            if i == 0:
                indicator_x = (start_x - ((square_size * word_length) - LETTER_X_SPACING )/ word_length) + (new_indicator.rect[2] / 2)
            elif i == 1:
                indicator_x = (start_x - ((square_size * word_length) - LETTER_X_SPACING )/ word_length) + (new_indicator.rect[2] * 1.6)
Indicator.draw_indicators()

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    # updates the indicators as well, and if all letters are green, the game is won.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    color_chagnging = indication.Indication(indicators, guesses)
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
    current_letter_bg_x = start_x

    # Checks if your out of guesses and havent guessed the correct word and end game.
    if guesses_count == max_guesses and game_result == "":
        game_result = "L"

def play_again():
    # Puts the play again text on the screen, genarates a box covering indicators.
    pygame.draw.rect(SCREEN, "white", (indicators[0].x, indicators[0].y, ((indicators[9].x - indicators[0].x) + square_size), ((indicators[-1].y - indicators[0].y) + square_size)))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, HEIGHT / 1.4))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD.upper()}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, HEIGHT / 1.2))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill(Background_color)
    guesses_count = 0
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[]] * max_guesses
    current_guess = []
    current_guess_string = ""
    game_result = ""
    draw_guide()

    guess_grid.draw_grid(SCREEN)
    Indicator.draw_indicators()

    pygame.display.update()

    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()

def create_new_letter():
    global current_guess_string, current_letter_bg_x, current_letter_bg_y, guesses_count

    current_guess_string += key_pressed
    current_letter_bg_y = start_y + guesses_count * (square_size + LETTER_Y_SPACING)    
    new_letter = text_box.Text_box(key_pressed, GUESSED_LETTER_FONT, square_size, BLACK, WHITE, OUTLINE, current_letter_bg_x, current_letter_bg_y, SCREEN)
    current_letter_bg_x = start_x + len(current_guess_string) * (square_size + LETTER_X_SPACING)    

    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x = start_x + len(current_guess_string) * (square_size + LETTER_X_SPACING)
    
# Game Loop
while True:
    if game_result != "":
        play_again()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) == word_length and current_guess_string.lower() in WORDS:
                        check_guess(current_guess)
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < word_length:
                        create_new_letter()