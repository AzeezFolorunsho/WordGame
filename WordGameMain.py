import pygame
import sys
import random
from words import *

# pygame setup
pygame.init()

# CONSTANT variables

WIDTH, HEIGHT = 1280, 720

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("assets/Starting Tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(317, 300))
ICON = pygame.image.load("assets/Icon.png")


pygame.display.set_caption("Worde Game!")
pygame.display.set_icon(ICON)

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

CORRECT_WORD = "coder"

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GESSED_LETTER_FONT = pygame.font.Font("assests/FreeSansBold.otf", 50)
AVALABLE_LETTER_FONT = pygame.font.Font("assests/FreeSansBold.otf", 25)

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75

# Global variables

guesses_count = 0

# max_guess_count limits total number of guesses
max_guess_count = 6

# guesses is a 2D list that will store guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses= [[]] * max_guess_count

current_guess = []
current_guess_string = ""
current_letter_bg_x = 110

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

game_result = ""
class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        pass
 
    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pass
 
    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pass
 
class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        pass
 
    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pass
 
# Drawing the indicators on the screen.
 
def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    pass
 
def play_again():
    # Puts the play again text on the screen.
    pass
 
def reset():
    # Resets all global variables to their default states.
    pass
 
def create_new_letter():
    # Creates a new letter and adds it to the guess.
    pass
 
def delete_letter():
    # Deletes the last letter from the guess.
    pass
 
while True:
    if game_result != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()