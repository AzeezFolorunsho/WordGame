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
from wordle_plus_game.src.games.timer import Timer, Countdown
from wordle_plus_game.src.utils.guides import Guide
from wordle_plus_game.src.utils.words import WORDS

class WordleHangman:
    """
    Class representing the Wordle Hangman game logic.

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
        self.guesses = []
        self.incorrect_attempts = 0
        self.max_attempts = 7
        self.game_outcome = ""
        self.score = 0
        self.game_time = 0

        # Initialize game components
        self.target_word = 'coder'  # set target word to 'coder' for testing purposes will change to random.choice(WORDS)
        self.is_indicating = True
        self.difficulty_level()
        self.correct_word_boxes = self.create_word_boxes()
        self.score_tracker = ScoreTracking()
        self.score_saved = False
        self.timer = Timer(self.screen, 30, self.screen_height / 2, self.bg_color, self.timer_font)
        self.timer.start()

        # Initialize the word and curent_guess grid
        self.word_grid = TextboxGrid(self.screen, self.textbox_size, 1, len(self.target_word), self.textbox_x_spacing, self.textbox_y_spacing, self.textbox_start_x, self.textbox_start_y, self.light_gray, self.white)
        self.word_grid.draw_underlined_grid()
        self.current_guess_grid = TextboxGrid(self.screen, self.textbox_size, 1, 1, 0, 0, self.current_guess_textbox_x, self.current_guess_textbox_y, self.light_gray, self.white)
        self.current_guess_grid.draw_grid()

        # Initialize the keyboard
        self.keyboard = OnScreenKeyboard(self.keyboard_start_x, self.keyboard_start_y, self.keyboard_x_spacing, self.keyboard_y_spacing, self.keyboard_width, self.keyboard_height, self.keyboard_font, self.white, self.light_gray, self.medium_gray)

        # Initialize the return button
        self.return_button = TextButton("Return", self.keyboard_font, self.white, self.black, self.light_gray, self.screen_width - 140, 27, 110, 45)

        # Load hangman images
        self.hangman_images = []
        for i in range(7 - self.max_attempts, 8):
            self.hangman_images.append(pygame.image.load(f"wordle_plus_game/assets/hangman_images/hangman{i}.png"))
        print(len(self.hangman_images))
        self.update_hangman_image()

        # Initialize guides (for testing purposes)
        self.guide = Guide(self.screen)
        self.guide.draw_third_guides(self.black)
        self.guide.draw_cross_guides(self.red)
        
        #  Difficulty level values
        self.difficulty_level = self.settings.get("Game Settings", "Current Difficulty Level")

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
        self.textbox_start_y = self.screen_height / 2
        self.textbox_x_spacing = 8
        self.textbox_y_spacing = 20

        # current guess textbox dimensions and positioning
        self.current_guess_textbox_x = (self.screen_width / 1.5) + self.textbox_size
        self.current_guess_textbox_y = self.screen_height / 3

        # Hangman image positioning
        self.hangman_image_x = 410
        self.hangman_image_y = 10

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
        pygame.display.set_caption("Wordle+ Hangman")
        self.screen.fill(self.bg_color)

    def difficulty_level(self):
        if self.difficulty == "Normal":     #default values
            self.target_word = "coder"
            # self.target_word = random_word(5)
        
        elif self.difficulty == "Easy":
            # self.target_word = random_word(4)
            self.target_word = "code"
            self.max_attempts = 7
        
        elif self.difficulty == "Hard":
            self.target_word = "coders"#random_word(6)    # May change into 6-8
            self.max_attempts = 4
            self.is_indicating = False
            # time incentive
            self.penalty_time = 30
            self.penalty_message = Text("Score multiplied after 30 seconds", self.timer_font, 30, self.screen_height / 2 + 50)
            self.penalty_message.draw(self.screen)
            self.score_multiplier = 7 #score multiplier value

        else: # Ultra hard
            self.target_word = "coders"#random_word(6)
            self.is_indicating = False
            self.max_attempts = 2
            # time incentive
            self.time_limit = 30
            self.countdown = Countdown(self.screen, 30, self.screen_height / 2, self.bg_color, self.timer_font, self.time_limit, text_color=self.red)
            self.penalty_message = Text("Time limit 30 seconds!", self.timer_font, 30, self.screen_height / 2 + 50)
            self.countdown.start()
            self.penalty_message.draw(self.screen)

    def create_word_boxes(self):
        """
        Creates text boxes for each letter in the target word.

        Returns:
            list: List of Textbox instances for each letter.
        """
        boxes = []
        current_x = self.textbox_start_x
        for letter in self.target_word:
            box = Textbox(letter.upper(), self.letter_font, self.textbox_size, self.black, self.white, self.light_gray, current_x, self.textbox_start_y, self.screen)
            boxes.append(box)
            current_x += self.textbox_size + self.textbox_x_spacing
        return boxes

    def update_textbox_color(self, index, letter, color):
        """
        Updates the background color of a given textbox and the on-screen keyboard key of the same letter.

        Args:
            index (int): The index of the letter in the correct word.
            letter (str): The letter to update.
            color (str): The color to set as the background.
        """
        self.keyboard.update_key_color(letter, color)
        # if self.difficulty != "Ultra Hard":
        self.correct_word_boxes[index].update_bg_color(letter, color)
        # If the commented code is used, then Ultra Hard Hangman isn't winnable due to how the wins are decided. Do we want indication in Ultra Hard?

    def evaluate_guess(self):
        """
        Evaluates the current guess and updates the game state.
        """
        letter_in_word = False
        game_won = True

        self.guesses.append(self.current_guess[-1].text)

        for i, box in enumerate(self.correct_word_boxes):
            letter_text = box.text.lower()

            if letter_text == self.current_guess[-1].text.lower():
                self.update_textbox_color(i, letter_text, self.green)
                if self.is_indicating:
                    box.draw()
                letter_in_word = True

        if not letter_in_word:
            self.keyboard.update_key_color(self.current_guess[-1].text, self.gray)
            self.incorrect_attempts += 1
            self.update_hangman_image()

        pygame.display.update()
        self.current_guess[-1].delete()
        self.current_guess.pop()

        for box in self.correct_word_boxes:
            if box.bg_color != self.green:
                game_won = False
                break

        if game_won:
            self.game_outcome = "W"
            for box in self.correct_word_boxes:
                if not self.is_indicating:
                    box.draw()
        elif self.incorrect_attempts == self.max_attempts:
            if self.difficulty == "Easy":
                self.incorrect_attempts = 0
            else:
                self.game_outcome = "L"
            for box in self.correct_word_boxes:
                if not self.is_indicating and box.bg_color == self.green:
                    box.draw()

    def reset_game(self):
        """
        Resets the game to start a new round.
        """
        self.screen.fill(self.bg_color) # clear screen

        self.target_word = random.choice(WORDS)
        self.current_guess = []
        self.guesses = []
        self.incorrect_attempts = 0
        self.game_outcome = ""
        self.score = 0
        self.game_time = 0
        self.score_saved = False

        self.correct_word_boxes = self.create_word_boxes()
        self.word_grid.draw_underlined_grid()
        self.current_guess_grid.draw_grid()
        self.keyboard.reset_key_colors()
        self.update_hangman_image()
        self.timer.start()

        pygame.display.update()

    def add_letter(self, letter):
        """
        Adds a new letter to the current guess and displays it on the screen.

        Args:
            letter (str): The letter to add.
        """
        self.current_guess.append(Textbox(letter, self.letter_font, self.textbox_size, self.black, self.white, self.light_gray, self.current_guess_textbox_x, self.current_guess_textbox_y, self.screen))
        self.current_guess[-1].draw()
        
    def is_invalid(self, letter):
        return letter in self.guesses if "Hard" not in self.difficulty else False

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
            self.score_tracker.save_score("Hangman", data, self.screen, self.top_score_font, top_score_x, top_score_y, self.bg_color, "New Top Score!")
            self.score_saved = True

    def update_hangman_image(self):
        """
        Updates the hangman image on the screen based on the number of incorrect attempts.
        """
        bg_rect = self.hangman_images[-1].get_rect(topleft = (self.hangman_image_x, self.hangman_image_y))
        bg_rect = bg_rect.scale_by(0.7)
        pygame.draw.rect(self.screen, self.bg_color, bg_rect)
        self.screen.blit(self.hangman_images[self.incorrect_attempts], (self.hangman_image_x, self.hangman_image_y))

    def game_loop(self, running):
        """
        The main game loop, handling events and updating the game state.

        Args:
            running (bool): A flag to indicate if the game is running.
        """
        while running:
            if not self.difficulty == "Ultra Hard":
                self.timer.draw()
            else:
                self.countdown.draw()
                if self.countdown.countdown_time == 0:
                    self.game_outcome = "L"
            # turns timer red if over penalty time
            if self.difficulty == "Hard" and self.timer.elapsed_time > self.penalty_time:
                self.timer.set_text_color(self.red)
                # score multiplier
            
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
                        if len(self.current_guess) == 1:
                            self.evaluate_guess()
                            if self.game_outcome:
                                self.game_time = self.timer.stop()
                                if self.difficulty == "Ultra Hard":
                                    self.game_time = self.countdown.stop()
                elif clicked_key == "DEL":
                    self.remove_letter()
                else:
                    if str(clicked_key) in "QWERTYUIOPASDFGHJKLZXCVBNM" and not self.game_outcome:
                        if len(self.current_guess) < 1 and not self.is_invalid(str(clicked_key)):
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
                            if len(self.current_guess) == 1:
                                self.evaluate_guess()
                                if self.game_outcome:
                                    self.game_time = self.timer.stop()
                                    if self.difficulty == "Ultra Hard":
                                        self.game_time = self.countdown.stop()
                    elif event.key == pygame.K_BACKSPACE:
                        self.remove_letter()
                    else:
                        if event.unicode.upper() in "QWERTYUIOPASDFGHJKLZXCVBNM" and not self.game_outcome:
                            if len(self.current_guess) < 1 and not self.is_invalid(event.unicode.upper()):
                                self.add_letter(event.unicode.upper())

            if self.game_outcome:
                result_message = "You won! =^)" if self.game_outcome == "W" else "You lost! =^("
                if self.game_outcome == "W":
                    self.score = self.game_time * self.incorrect_attempts + 1
                    self.conclude_game()
                game_results = GameResults(20, 20, self.result_font, bg_color=self.bg_color, finish_message=result_message, score=str(self.score), word_reveal=[self.target_word])
                game_results.draw_results(self.screen)

            pygame.display.flip()
