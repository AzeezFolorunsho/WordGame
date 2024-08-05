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
from Funtions.guides import Guide  # Temporary import for testing

class GridManager:
    def __init__(self, screen, textbox_size, max_guesses, word_length, x_spacing, y_spacing, start_x, start_y, grid_color, bg_color):
        self.screen = screen
        self.textbox_size = textbox_size
        self.max_guesses = max_guesses
        self.word_length = word_length
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.start_x = start_x
        self.start_y = start_y
        self.grid_color = grid_color
        self.bg_color = bg_color
        self.grid = Textbox_grid(textbox_size, max_guesses, word_length, x_spacing, y_spacing, start_x, start_y, grid_color, bg_color)

    def draw_grid(self):
        self.grid.draw_grid(self.screen)

class KeyboardManager:
    def __init__(self, screen, start_x, start_y, x_spacing, y_spacing, width, height, font, key_color, inactive_color, active_color, alphabet):
        self.screen = screen
        self.alphabet = alphabet
        self.inactive_color = inactive_color
        self.keyboard = On_Screen_Keyboard(start_x, start_y, x_spacing, y_spacing, width, height, font, key_color, inactive_color, active_color)

    def draw_keyboard(self):
        for key in self.keyboard.key_button_list:
            key.draw(self.screen)

    def update_key_color(self, letter, color):
        self.keyboard.update_bg_color(letter, color)

    def reset_key_color(self):
        for letter in self.alphabet:
            self.keyboard.update_bg_color(letter, self.inactive_color)

class WordleClassic:
    def __init__(self):
        self.setup_constants()
        self.setup_pygame()

        # Initialize game components
        self.correct_word = random.choice(WORDS)
        self.correct_word_length = len(self.correct_word)

        self.guesses_count = 0
        self.guesses = [[] for _ in range(self.MAX_GUESSES)]
        self.current_guess = []
        self.current_guess_string = ""
        
        self.game_result = ""
        self.indicate = True

        self.current_textbox_x = self.TEXTBOX_START_X
        self.current_textbox_y = self.TEXTBOX_START_Y

        self.score = 100

        self.grid_manager = GridManager(
            self.SCREEN, self.TEXTBOX_SIZE, self.MAX_GUESSES, 
            self.correct_word_length, self.TEXTBOX_X_SPACING, 
            self.TEXTBOX_Y_SPACING, self.TEXTBOX_START_X, 
            self.TEXTBOX_START_Y, self.LIGHT_GREY, self.WHITE
        )
        self.grid_manager.draw_grid()

        self.keyboard_manager = KeyboardManager(
            self.SCREEN, self.ON_SCREEN_KEYBOARD_START_X, 
            self.ON_SCREEN_KEYBOARD_START_Y, self.ON_SCREEN_KEYBOARD_X_SPACING, 
            self.ON_SCREEN_KEYBOARD_Y_SPACING, self.ON_SCREEN_KEYBOARD_WIDTH, 
            self.ON_SCREEN_KEYBOARD_HEIGHT, self.ON_SCREEN_KEYBOARD_FONT, 
            self.WHITE, self.LIGHT_GREY, self.MEDIUM_GREY, self.ALPHABET
        )

        self.return_button = Text_Button(
            "Return", self.ON_SCREEN_KEYBOARD_FONT, 
            self.BLACK, self.GREY, self.LIGHT_GREY, 
            self.SCREEN_WIDTH - 100, 15, 100, 40
        )

        self.guide = Guide(self.SCREEN)
        self.guide.draw_guides_thirds(self.BLACK)
        self.guide.draw_guides_cross(self.RED)

    def setup_constants(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.TEXTBOX_SIZE = 62.4
        self.MAX_GUESSES = 6

        self.ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"

        # Colors
        self.WHITE = "#FFFFFF"
        self.BLACK = "#000000"
        self.GREY = "#787c7e"
        self.LIGHT_GREY = "#d3d6da"
        self.MEDIUM_GREY = "#878a8c"
        self.GREEN = "#6aaa64"
        self.YELLOW = "#c9b458"
        self.RED = "#FF0000"
        self.BACKGROUND_COLOR = self.WHITE

        # Textbox
        self.TEXTBOX_START_X = 468
        self.TEXTBOX_START_Y = 3.6
        self.TEXTBOX_X_SPACING = 8
        self.TEXTBOX_Y_SPACING = 20

        # On-Screen Keyboard
        self.ON_SCREEN_KEYBOARD_START_X = self.SCREEN_WIDTH / 3.3
        self.ON_SCREEN_KEYBOARD_START_Y = self.SCREEN_HEIGHT / 1.47
        self.ON_SCREEN_KEYBOARD_X_SPACING = 10
        self.ON_SCREEN_KEYBOARD_Y_SPACING = 20
        self.ON_SCREEN_KEYBOARD_WIDTH = self.TEXTBOX_SIZE / 1.5
        self.ON_SCREEN_KEYBOARD_HEIGHT = self.TEXTBOX_SIZE

        # Fonts
        self.GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
        self.ON_SCREEN_KEYBOARD_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
        self.GAME_RESULTS_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)

    def setup_pygame(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.icon = pygame.image.load("assets/wordle+logo.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Wordle+ Classic")

        self.SCREEN.fill(self.BACKGROUND_COLOR)

    def update_guesses_bg_color(self, index, letter, color):
        if self.indicate:
            self.keyboard_manager.update_key_color(letter, color)
            self.current_guess[index].update_bg_color(letter, color)

    def check_guess(self):
        game_decided = False

        for i in range(len(self.current_guess)):
            lowercase_letter = self.current_guess[i].text.lower()
            
            if lowercase_letter in self.correct_word:
                if lowercase_letter == self.correct_word[i]:
                    self.update_guesses_bg_color(i, lowercase_letter, self.GREEN)
                    if not game_decided:
                        self.game_result = "W"
                else:
                    self.update_guesses_bg_color(i, lowercase_letter, self.YELLOW)
                    self.game_result = ""
                    game_decided = True
            else:
                self.update_guesses_bg_color(i, lowercase_letter, self.GREY)
                self.game_result = ""
                game_decided = True
            
            pygame.display.update()
        
        self.guesses_count += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.current_textbox_x = self.TEXTBOX_START_X

        if self.guesses_count == self.MAX_GUESSES and self.game_result == "":
            self.game_result = "L"

    def reset(self):
        self.SCREEN.fill(self.BACKGROUND_COLOR)
        
        self.guesses_count = 0
        self.correct_word = random.choice(WORDS)
        self.guesses = [[] for _ in range(self.MAX_GUESSES)]
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = ""
        self.current_textbox_x = self.TEXTBOX_START_X
        self.current_textbox_y = self.TEXTBOX_START_Y

        self.grid_manager.draw_grid()

        self.keyboard_manager.reset_key_color()

        pygame.display.update()

    def create_new_letter(self, letter):
        self.current_guess_string += letter
        self.current_textbox_y = self.TEXTBOX_START_Y + self.guesses_count * (self.TEXTBOX_SIZE + self.TEXTBOX_Y_SPACING)
        new_letter = Textbox(letter, self.GUESSED_LETTER_FONT, self.TEXTBOX_SIZE, self.BLACK, self.WHITE, self.LIGHT_GREY, self.current_textbox_x, self.current_textbox_y, self.SCREEN)
        self.current_textbox_x = self.TEXTBOX_START_X + len(self.current_guess_string) * (self.TEXTBOX_SIZE + self.TEXTBOX_X_SPACING)

        self.guesses[self.guesses_count].append(new_letter)
        self.current_guess.append(new_letter)

        for guess in self.guesses:
            for letter in guess:
                letter.draw()

    def delete_letter(self):
        self.guesses[self.guesses_count][-1].delete()
        self.guesses[self.guesses_count].pop()

        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()
        self.current_textbox_x = self.TEXTBOX_START_X + len(self.current_guess_string) * (self.TEXTBOX_SIZE + self.TEXTBOX_X_SPACING)

    def game_loop(self):
        while True:
            if self.return_button.draw(self.SCREEN):
                print("Return to Menu")
                self.SCREEN.fill(self.WHITE)
                self.reset()

                return  # Exit the game loop and return to the menu

            # On-screen keyboard events
            for keys in self.keyboard_manager.keyboard.key_button_list:
                button_clicked = keys.draw(self.SCREEN)

                if button_clicked == "ENT":
                    if self.game_result != "":
                        self.reset()
                    else:
                        if len(self.current_guess_string) == self.correct_word_length and self.current_guess_string.lower() in WORDS:
                            self.check_guess()
                elif button_clicked == "DEL":
                    if len(self.current_guess_string) > 0:
                        self.delete_letter()
                else:
                    if str(button_clicked) in self.ALPHABET:
                        letter_pressed = button_clicked.upper()
                        if len(self.current_guess_string) < self.correct_word_length:
                            self.create_new_letter(letter_pressed)

            # Keyboard events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.game_result != "":
                            self.reset()
                        else:
                            if len(self.current_guess_string) == self.correct_word_length and self.current_guess_string.lower() in WORDS:
                                self.check_guess()
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.current_guess_string) > 0:
                            self.delete_letter()
                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in self.ALPHABET and key_pressed != "":
                            if len(self.current_guess_string) < self.correct_word_length:
                                self.create_new_letter(key_pressed)

            if self.game_result != "":
                if self.game_result == "W":
                    game_results_obj = Game_Results(20, 20, self.GAME_RESULTS_FONT, self.BLACK, self.WHITE, "You won! =^)", str(self.score), "Press ENTER to Play Again!", self.correct_word)
                else:
                    game_results_obj = Game_Results(20, 20, self.GAME_RESULTS_FONT, self.BLACK, self.WHITE, "You Lost! =^(", str(self.score), "Press ENTER to Play Again!", self.correct_word)

                game_results_obj.draw_results(self.SCREEN)

            pygame.display.flip()
