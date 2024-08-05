import pygame
import sys
import random
from words import WORDS
from Funtions.text import Text
from Funtions.textbox_grid import Textbox_grid
from Funtions.textbox import Textbox
from Funtions.buttons import Text_Button
from Funtions.on_screen_keyboard import On_Screen_Keyboard
from Funtions.game_results import Game_Results

# Temporary imports for testing
from Funtions.guides import Guide

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

TEXTBOX_SIZE = 62.4

correct_word_length = 0

current_textbox_x = 0
current_textbox_y = 0

guesses_count = 0
max_guesses = 6

guesses = [[] for _ in range(max_guesses)]
current_guess = []
current_guess_string = ""
indicate = True
game_result = ""
score = 100 #temporary score


def play_classic():
    global current_guess_string, current_textbox_x, current_textbox_y, guesses_count, guesses, current_guess, game_result    

    # Initialize pygame
    pygame.init()

    # Constants
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ICON = pygame.image.load("assets/wordle+logo.png")
    pygame.display.set_icon(ICON)
    pygame.display.set_caption("Wordle+ Classic")

    # Colors
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GREY = "#787c7e"
    LIGHT_GREY = "#d3d6da"
    MEDIUM_GREY = "#878a8c"
    GREEN = "#6aaa64"
    YELLOW = "#c9b458"
    RED = "#FF0000"
    BACKGROUND_COLOR = WHITE

    # Fill the screen with background color
    SCREEN.fill(BACKGROUND_COLOR)

    # Correct word for testing, change to random.choice(WORDS) for production
    CORRECT_WORD = "coder"

    # Fonts
    GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
    ON_SCREEN_KEYBOARD_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
    GAME_RESULTS_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)

    # Alphabet
    ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"

    # Textbox settings
    TEXTBOX_START_X = 468
    TEXTBOX_START_Y = 3.6
    TEXTBOX_X_SPACING = 8
    TEXTBOX_Y_SPACING = 20
    
    # On-screen keyboard settings
    ON_SCREEN_KEYBOARD_START_X = SCREEN_WIDTH / 3.3
    ON_SCREEN_KEYBOARD_START_Y = SCREEN_HEIGHT / 1.47
    ON_SCREEN_KEYBOARD_X_SPACING = 10
    ON_SCREEN_KEYBOARD_Y_SPACING = 20
    ON_SCREEN_KEYBOARD_WIDTH = TEXTBOX_SIZE / 1.5
    ON_SCREEN_KEYBOARD_HEIGHT = TEXTBOX_SIZE

    # Global Variables
    current_textbox_x = TEXTBOX_START_X
    current_textbox_y = TEXTBOX_START_Y

    correct_word_length = len(CORRECT_WORD)

    # Game Objects
    guides_obj = Guide(SCREEN)
    guides_obj.draw_guides_cross(BLACK)
    guides_obj.draw_guides_thirds(RED)

    textbox_grid_obj = Textbox_grid(TEXTBOX_SIZE, max_guesses, correct_word_length, TEXTBOX_X_SPACING, TEXTBOX_Y_SPACING, TEXTBOX_START_X, TEXTBOX_START_Y, LIGHT_GREY, WHITE)
    textbox_grid_obj.draw_grid(SCREEN)

    on_screen_keyboard_obj = On_Screen_Keyboard(ON_SCREEN_KEYBOARD_START_X, ON_SCREEN_KEYBOARD_START_Y, ON_SCREEN_KEYBOARD_X_SPACING, ON_SCREEN_KEYBOARD_Y_SPACING, ON_SCREEN_KEYBOARD_WIDTH, ON_SCREEN_KEYBOARD_HEIGHT, ON_SCREEN_KEYBOARD_FONT, WHITE, LIGHT_GREY, MEDIUM_GREY)

    return_button_obj = Text_Button("Return", ON_SCREEN_KEYBOARD_FONT, BLACK, GREY, LIGHT_GREY, SCREEN_WIDTH - 100, 15, 100, 40)

    # Functions
    def update_guesses_bg_color(index, letter, color):
        if indicate:
            on_screen_keyboard_obj.update_bg_color(letter, color)
            current_guess[index].update_bg_color(letter, color)

    def check_guess():
        global current_guess, current_guess_string, guesses_count, current_textbox_x, game_result

        game_decided = False

        for i in range(len(current_guess)):
            lowercase_letter = current_guess[i].text.lower()
            
            if lowercase_letter in CORRECT_WORD:
                if lowercase_letter == CORRECT_WORD[i]:
                    update_guesses_bg_color(i, lowercase_letter, GREEN)
                    if not game_decided:
                        game_result = "W"
                else:
                    update_guesses_bg_color(i, lowercase_letter, YELLOW)
                    game_result = ""
                    game_decided = True
            else:
                update_guesses_bg_color(i, lowercase_letter, GREY)
                game_result = ""
                game_decided = True
            
            pygame.display.update()
        
        guesses_count += 1
        current_guess = []
        current_guess_string = ""
        current_textbox_x = TEXTBOX_START_X

        if guesses_count == max_guesses and game_result == "":
            game_result = "L"

    def reset():
        global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
        SCREEN.fill(BACKGROUND_COLOR)
        guesses_count = 0
        CORRECT_WORD = random.choice(WORDS)
        guesses = [[] for _ in range(max_guesses)]
        current_guess = []
        current_guess_string = ""
        game_result = ""

        textbox_grid_obj.draw_grid(SCREEN)

        for letter in ALPHABET:
            on_screen_keyboard_obj.update_bg_color(letter, LIGHT_GREY)

        pygame.display.update()

    def create_new_letter(letter):
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
        global current_guess_string, current_textbox_x
        guesses[guesses_count][-1].delete()
        guesses[guesses_count].pop()

        current_guess_string = current_guess_string[:-1]
        current_guess.pop()
        current_textbox_x = TEXTBOX_START_X + len(current_guess_string) * (TEXTBOX_SIZE + TEXTBOX_X_SPACING)

    # Game Loop
    while True:

        if return_button_obj.draw(SCREEN):
            print("Return to Menu")
        # On-screen keyboard events
        for keys in on_screen_keyboard_obj.key_button_list:
            button_clicked = keys.draw(SCREEN)
            
            if button_clicked == "ENT":
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) == correct_word_length and current_guess_string.lower() in WORDS:
                        check_guess()
            elif button_clicked == "DEL":
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                if str(button_clicked) in ALPHABET:
                    letter_pressed = button_clicked.upper()
                    if len(current_guess_string) < correct_word_length:
                        create_new_letter(letter_pressed)

        # Keyboard events
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
                            check_guess()
                elif event.key == pygame.K_BACKSPACE:
                    if len(current_guess_string) > 0:
                        delete_letter()
                else:
                    key_pressed = event.unicode.upper()
                    if key_pressed in ALPHABET and key_pressed != "":
                        if len(current_guess_string) < correct_word_length:
                            create_new_letter(key_pressed)

        if game_result != "":
            if game_result == "W":
                game_results_obj = Game_Results(20, 20, GAME_RESULTS_FONT, BLACK, WHITE, "You won! =^)", str(score), "Press ENTER to Play Again!", CORRECT_WORD)
            else:
                game_results_obj = Game_Results(20, 20, GAME_RESULTS_FONT, BLACK, WHITE, "You Lost! =^(", str(score), "Press ENTER to Play Again!", CORRECT_WORD)
            
            game_results_obj.draw_results(SCREEN)
        
        pygame.display.flip()
