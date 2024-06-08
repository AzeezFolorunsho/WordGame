import pygame
import sys
import random
from indicators import *
from words import *

# initiates pygame session allowing pygame functions to be used.
pygame.init()

# CONSTANTS

WIDTH, HEIGHT = 1280, 720

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# geneates little logo and icon in top left corner.
ICON = pygame.image.load("assets/wordle+logo.png")
pygame.display.set_icon(ICON)
pygame.display.set_caption("Wordle+ !")

# COLORS
WHITE = "#FFFFFF"
BLACK = "#000000"
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

# tempraraly "coder" for testing purposes, change to random.choice(WORDS).
CORRECT_WORD = "coder"

SCREEN.fill(WHITE)
# SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()

# defines the size of leters and spacing between letter boxes in the grid.
LETTER_SIZE = 25
LETTER_BOX_SIZE = LETTER_SIZE * 2
LETTER_BOX_X_SPACING = LETTER_BOX_SIZE * 1.4
LETTER_BOX_Y_SPACING = LETTER_BOX_SIZE // 2

# inisilizes the font of the guessed letter.
GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", LETTER_SIZE)


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

# defines where the first letter will be drawn on the x and y axis.
STARTING_LETTER_BG_X = (WIDTH - LETTER_BOX_SIZE * word_length) / 2
STARTING_LETTER_BG_Y = (HEIGHT - (LETTER_BOX_SIZE * max_guesses)) / 8

# current_letter_bg_x is used to keep track of where the next letter will be drawn.
current_letter_bg_x = STARTING_LETTER_BG_X

# game_result is used to keep track of if the game has been won or not.
game_result = ""

# inisilaising indicator
Indicator.draw_indicators(SCREEN, STARTING_LETTER_BG_X, HEIGHT - (STARTING_LETTER_BG_Y * max_guesses) - 100)
# indicat.draw_indicators()
# indicators_rect = ((starting_x, starting_y), (len(ALPHABET[0]) * LETTER_BOX_SIZE, len(ALPHABET) * LETTER_BOX_SIZE))

# GAME FUNCTIONS

# temporary guides for checking alingment.
def draw_guide():
    center_line_x = pygame.draw.rect(SCREEN, "black", ((0, HEIGHT/2), (WIDTH, 2)))
    center_line_y = pygame.draw.rect(SCREEN, "black", ((WIDTH/2, 0), (2, HEIGHT)))
draw_guide()

# draws the empty grid of squares on the screen basesed on the lenggth of the word and the number of guesses.
class Grid():
    # global square_size

    # Calculate the starting position of the grid.
    start_x = (WIDTH - LETTER_BOX_SIZE * word_length) / 2
    start_y = (HEIGHT - LETTER_BOX_SIZE * max_guesses) / 30

    @staticmethod
    def draw_grid(square_size = LETTER_BOX_SIZE, start_x = start_x, start_y = start_y):
        # Draw the squares.
        for i in range(max_guesses):
            y = start_y
            y += i * (square_size + LETTER_BOX_Y_SPACING)
            for j in range(word_length):
                x = start_x + (j % word_length) * (square_size + LETTER_BOX_X_SPACING - 65)
                pygame.draw.rect(SCREEN, WHITE, (x, y, square_size, square_size))
                pygame.draw.rect(SCREEN, OUTLINE, (x, y, square_size, square_size), 3)
    pygame.display.update()
Grid.draw_grid()

# create individual letters that can be added to a word guess in the game.
class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (self.bg_x, self.bg_y, LETTER_BOX_SIZE, LETTER_BOX_SIZE)
        self.text = text
        self.text_position = (self.bg_x+30, self.bg_y+30)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    # updates the indicators as well, and if all letters are green, the game is won.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(word_length):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for indicator in indicators:
                    indicator.update(lowercase_letter, GREEN)
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for indicator in indicators:
                    indicator.update(lowercase_letter, YELLOW)
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for indicator in indicators:
                indicator.update(lowercase_letter, GREY)
            game_result = ""
            game_decided = True
        
        # chanes text color to white for better contrast and updates the text and screen.
        guess_to_check[i].text_color = "white"
        guess_to_check[i].draw()
        pygame.display.update()
    
    # incraments the number of guesses and resets the current guess for the next guess.
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = STARTING_LETTER_BG_X

    # Checks if your out of guesses and havent guessed the correct word and end game.
    if guesses_count == max_guesses and game_result == "":
        game_result = "L"

def play_again():
    # Puts the play again text on the screen, genarates a box covering indicators.
    pygame.draw.rect(SCREEN, WHITE, (indicators[0].x, indicators[0].y, ((indicators[9].x - indicators[0].x) + (LETTER_BOX_SIZE - 10)), ((indicators[-1].y - indicators[0].y) + (LETTER_BOX_SIZE + 10))))
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
    SCREEN.fill("white")
    # SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    guesses_count = 0
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[]] * max_guesses
    current_guess = []
    current_guess_string = ""
    game_result = ""
    draw_guide()

    Grid.draw_grid()
    Indicator.draw_indicators()

    pygame.display.update()

    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*80 + LETTER_BOX_Y_SPACING))
    current_letter_bg_x += LETTER_BOX_X_SPACING 
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
    current_letter_bg_x -= LETTER_BOX_X_SPACING

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