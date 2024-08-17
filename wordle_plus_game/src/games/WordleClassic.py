import pygame
import random
import sys
from wordle_plus_game.src.core.score_tracking import ScoreTracking
from wordle_plus_game.src.components.text import Text
from wordle_plus_game.src.components.textbox import Textbox
from wordle_plus_game.src.components.textbox_grid import TextboxGrid
from wordle_plus_game.src.components.buttons import TextButton
from wordle_plus_game.src.components.on_screen_keyboard import OnScreenKeyboard
from wordle_plus_game.src.games.game_results import GameResults
from wordle_plus_game.src.games.timer import Timer
from wordle_plus_game.src.utils.guides import Guide
from wordle_plus_game.src.utils.random_word import RandomWord

class WordleClassic:
    """
    Class representing the Wordle Classic game logic.

    Attributes:
        settings (Settings): Game settings.
        score_tracker (ScoreTracking): Score tracking for the game.
        timer (Timer): Timer for the game.
    """

    def __init__(self, settings):
        self.settings = settings
        self.init_constants()
        self.init_pygame()

        # Game state variables
        self.current_guess = []
        self.current_attempt = 0
        self.max_attempts = 6
        self.game_outcome = ""
        self.score = 0
        self.game_time = 0

        # Initialize game components
        self.random_words = RandomWord()
        self.target_word = 'coder'  # set target word to 'coder' for testing purposes will change to self.random_word.get_random_word(5)
        self.score_tracker = ScoreTracking()
        self.score_saved = False
        self.timer = Timer(self.screen, 30, self.screen_height / 2, self.bg_color, self.timer_font)
        self.timer.start()

        # Initialize the grid and keyboard
        self.textbox_grid = TextboxGrid(self.screen, self.textbox_size, self.max_attempts, len(self.target_word), self.textbox_x_spacing, self.textbox_y_spacing, self.textbox_start_x, self.textbox_start_y, self.light_gray, self.white)
        self.textbox_grid.draw_grid()
        self.keyboard = OnScreenKeyboard(self.keyboard_start_x, self.keyboard_start_y, self.keyboard_x_spacing, self.keyboard_y_spacing, self.keyboard_width, self.keyboard_height, self.keyboard_font, self.white, self.light_gray, self.medium_gray)

        # Initialize the return button
        self.return_button = TextButton("Return", self.keyboard_font, self.white, self.black, self.light_gray, self.screen_width - 140, 27, 110, 45)

        # Initialize guides (for testing purposes)
        self.guides = Guide(self.screen)
        # self.guides.draw_third_guides(self.black)
        # self.guides.draw_cross_guides(self.red)

    def init_constants(self):
        """
        Sets up the constants for the game.
        """
        self.screen_width = self.settings.get("General", "Screen Dimensions", {}).get("width", 1280)
        self.screen_height = self.settings.get("General", "Screen Dimensions", {}).get("height", 720)
        self.bg_color = self.settings.get("General", "Background Color", "#FFFFFF")
        self.difficulty = self.settings.get("Game Settings", "Current Difficulty Level", "Normal")

        # Colors
        self.white = "#FFFFFF"
        self.black = "#000000"
        self.gray = "#787c7e"
        self.light_gray = "#d3d6da"
        self.medium_gray = "#878a8c"
        self.green = "#6aaa64"
        self.yellow = "#c9b458"
        self.red = "#FF0000"

        # Textbox dimensions and positioning
        self.textbox_size = 62.4
        self.textbox_start_x = 468
        self.textbox_start_y = 3.6
        self.textbox_x_spacing = 8
        self.textbox_y_spacing = 20

        # On-screen keyboard dimensions and positioning
        self.keyboard_start_x = self.screen_width / 3.3
        self.keyboard_start_y = self.screen_height / 1.47
        self.keyboard_x_spacing = 10
        self.keyboard_y_spacing = 20
        self.keyboard_width = self.textbox_size / 1.5
        self.keyboard_height = self.textbox_size

        # Fonts
        self.letter_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 50)
        self.keyboard_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 25)
        self.result_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 30)
        self.timer_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 30)
        self.top_score_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 30)

    def init_pygame(self):
        """
        Initializes Pygame, sets up the screen, and loads the game icon.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.icon = pygame.image.load("wordle_plus_game/assets/wordle+logo.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Wordle+ Classic")
        self.screen.fill(self.bg_color)

    def update_textbox_color(self, index, letter, color):
        """
        Updates the background color of a given textbox and the on-screen keyboard key of the same letter.

        Args:
            index (int): The index of the letter in the current guess.
            letter (str): The letter to update.
            color (str): The color to set as the background.
        """
        self.keyboard.update_key_color(letter, color)
        self.current_guess[index].update_bg_color(letter, color)

    def evaluate_guess(self):
        """
        Evaluates the current guess and updates the game state.
        """
        game_lost = False

        for i, letter in enumerate(self.current_guess):
            letter_text = letter.text.lower()

            if letter_text in self.target_word:
                if letter_text == self.target_word[i]:
                    self.update_textbox_color(i, letter_text, self.green)
                    if not game_lost:
                        self.game_outcome = "W"
                else:
                    self.update_textbox_color(i, letter_text, self.yellow)
                    self.game_outcome = ""
                    game_lost = True
            else:
                self.update_textbox_color(i, letter_text, self.gray)
                self.game_outcome = ""
                game_lost = True

            pygame.display.update()

        self.current_attempt += 1
        self.current_guess = []

        if self.current_attempt == self.max_attempts and not self.game_outcome:
            self.game_outcome = "L"

    def reset_game(self):
        """
        Resets the game to start a new round.
        """
        self.screen.fill(self.bg_color)
        self.target_word = self.random_words.get_random_word(len(self.target_word))
        self.current_attempt = 0
        self.guesses = [[] for _ in range(self.max_attempts)]
        self.current_guess = []
        self.game_outcome = ""
        self.score = 0
        self.game_time = 0
        self.score_saved = False

        self.textbox_grid.draw_grid()
        self.keyboard.reset_key_colors()
        self.timer.start()

        pygame.display.update()

    def add_letter(self, letter):
        """
        Adds a new letter to the current guess and displays it on the screen.

        Args:
            letter (str): The letter to add.
        """
        self.current_guess.append(Textbox(letter, self.letter_font, self.textbox_size, self.black, self.white, self.light_gray, len(self.current_guess) * (self.textbox_size + self.textbox_x_spacing) + self.textbox_start_x, self.current_attempt * (self.textbox_size + self.textbox_y_spacing) + self.textbox_start_y, self.screen))
        self.current_guess[-1].draw()

    def remove_letter(self):
        """
        Removes the last letter in the current guess and clears its display.
        """
        if self.current_guess:
            self.current_guess.pop().delete()

    def conclude_game(self):
        """
        Handles the end of the game, saving the score and checking for a new top score.
        """
        data = {
            "Difficulty": self.difficulty,
            "Score": self.score,
            "Time": self.game_time
        }

        top_score_x = self.screen_width / 2
        top_score_y = self.screen_height / 2
        
        if not self.score_saved:
            self.score_tracker.save_score("Classic", data, self.screen, self.top_score_font, top_score_x, top_score_y, self.bg_color, "New Top Score!")
            self.score_saved = True

    def game_loop(self, running):
        """
        The main game loop, handling events and updating the game state.

        Args:
            running (bool): A flag to indicate if the game is running.
        """
        while running:
            self.timer.draw()

            if self.return_button.draw(self.screen):
                print("Return to Menu")
                self.reset_game()
                running = False
                return

            for keys in self.keyboard.key_buttons:
                clicked_key = keys.draw(self.screen)

                if clicked_key == "ENT":
                    if self.game_outcome:
                        self.reset_game()
                    else:
                        if len(self.current_guess) == len(self.target_word) and "".join([g.text for g in self.current_guess]).lower() in self.random_words.full_word_list:
                            self.evaluate_guess()
                            if self.game_outcome:
                                self.game_time = self.timer.stop()
                elif clicked_key == "DEL":
                    self.remove_letter()
                else:
                    if str(clicked_key) in "QWERTYUIOPASDFGHJKLZXCVBNM" and not self.game_outcome:
                        if len(self.current_guess) < len(self.target_word):
                            self.add_letter(clicked_key.upper())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.game_outcome:
                            self.reset_game()
                        else:
                            if len(self.current_guess) == len(self.target_word) and "".join([g.text for g in self.current_guess]).lower() in self.random_words.full_word_list:
                                self.evaluate_guess()
                                if self.game_outcome:
                                    self.game_time = self.timer.stop()
                    elif event.key == pygame.K_BACKSPACE:
                        self.remove_letter()
                    else:
                        if event.unicode.upper() in "QWERTYUIOPASDFGHJKLZXCVBNM" and not self.game_outcome:
                            if len(self.current_guess) < len(self.target_word):
                                self.add_letter(event.unicode.upper())

            if self.game_outcome:
                result_message = "You won! =^)" if self.game_outcome == "W" else "You Lost! =^("
                if self.game_outcome == "W":
                    self.score = self.game_time * self.current_attempt + 1
                    self.conclude_game()
                game_results = GameResults(20, 20, self.result_font, bg_color=self.bg_color, finish_message=result_message, score=str(self.score), word_reveal=[self.target_word])
                game_results.draw_results(self.screen)

            pygame.display.flip()
