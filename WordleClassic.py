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
from Funtions.timer import Timer
from Funtions.guides import Guide  # Temporary import for testing


class WordleClassic:
    def __init__(self):
        # Initialize Constants and pygame
        self.setup_constants()
        self.setup_pygame()
        
        ################################### Global Variables (will be accesed and changed througout the game) ###################################
        
        # sets the correct word
        self.correct_word = "coder" # hardcoded for testing, will be replaced with: random.choice(WORDS)
        self.correct_word_length = len(self.correct_word)
        # tracks the guesses
        self.guesses_count = 0
        self.guesses = [[] for _ in range(self.MAX_GUESSES)]
        self.current_guess = []
        self.current_guess_string = ""
        # tracks the game result "W" = Win, "L" = Loss, "" = undesided
        self.game_result = ""
        # tracks the score
        self.score = 0
        # sets the current textbox position
        self.current_textbox_x = self.TEXTBOX_START_X
        self.current_textbox_y = self.TEXTBOX_START_Y
        # tracks the duration for each round
        self.game_duration = 0
        
        # Initialize game objects

        self.game_timer = Timer(self.SCREEN, 30, self.SCREEN_HEIGHT / 2, self.BACKGROUND_COLOR)
        self.game_timer.activate_timer()
        
        self.textbox_grid_obj = Textbox_grid(
            self.SCREEN, self.TEXTBOX_SIZE, self.MAX_GUESSES, 
            self.correct_word_length, self.TEXTBOX_X_SPACING, 
            self.TEXTBOX_Y_SPACING, self.TEXTBOX_START_X, 
            self.TEXTBOX_START_Y, self.LIGHT_GREY, self.WHITE
        )
        # Draws the grid
        self.textbox_grid_obj.draw_grid()

        self.on_screen_keyboard_obj = On_Screen_Keyboard(
            self.KEYBOARD_START_X, self.KEYBOARD_START_Y, 
            self.KEYBOARD_X_SPACING, self.KEYBOARD_Y_SPACING, 
            self.KEYBOARD_WIDTH, self.KEYBOARD_HEIGHT, 
            self.ON_SCREEN_KEYBOARD_FONT, self.WHITE, 
            self.LIGHT_GREY, self.MEDIUM_GREY
        )

        self.return_button = Text_Button(
            "Return", self.ON_SCREEN_KEYBOARD_FONT, 
            self.WHITE, self.BLACK, self.LIGHT_GREY, 
            self.SCREEN_WIDTH - 140, 27, 110, 45
        )

        self.guide = Guide(self.SCREEN)
        self.guide.draw_guides_thirds(self.BLACK)
        self.guide.draw_guides_cross(self.RED)

    def setup_constants(self):
        ################################### CONSTANTS (will not change throughout the game) ###################################
        
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720 # Screen Dimensions
        self.IS_INDICATING = True # determines if the color of the textboxes and key board should change
        self.ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM" # alphabet for checking if the key typed or click is a letter
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
        # the maximum number of guesses
        self.MAX_GUESSES = 6
        # Textbox Dimensions
        self.TEXTBOX_SIZE = 62.4
        self.TEXTBOX_START_X = 468
        self.TEXTBOX_START_Y = 3.6
        self.TEXTBOX_X_SPACING = 8
        self.TEXTBOX_Y_SPACING = 20
        # On Screen Keyboard Dimensions
        self.KEYBOARD_START_X = self.SCREEN_WIDTH / 3.3
        self.KEYBOARD_START_Y = self.SCREEN_HEIGHT / 1.47
        self.KEYBOARD_X_SPACING = 10
        self.KEYBOARD_Y_SPACING = 20
        self.KEYBOARD_WIDTH = self.TEXTBOX_SIZE / 1.5
        self.KEYBOARD_HEIGHT = self.TEXTBOX_SIZE
        # Fonts
        self.GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
        self.ON_SCREEN_KEYBOARD_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
        self.GAME_RESULTS_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)
        self.TIMER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)

    def setup_pygame(self):
        # initialize pygame, screen, and icon
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # set icon and caption
        self.icon = pygame.image.load("assets/wordle+logo.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Wordle+ Classic")
        # fills screen with white
        self.SCREEN.fill(self.BACKGROUND_COLOR)

    def update_guesses_bg_color(self, index, letter, color):
        # updates the background color of a given textbox and the on screen keyboard key of the same letter to the given color
        if self.IS_INDICATING:
            self.on_screen_keyboard_obj.update_key_color(letter, color)
            self.current_guess[index].update_bg_color(letter, color)

    def check_guess(self):
        # checks if the current guess is the correct
        
        game_decided = False # used to determine if the game has been lost, if any letters are not in the correct word at the correct place

        # loops through each letter in the current guess and updates the background color accordingly
        # also checks if the game has been won or lost based on if all letters in the current guess are in the correct word at the corect place
        for i in range(len(self.current_guess)):
            
            current_letter = self.current_guess[i].text.lower() # converts the current letter to lowercase beacuse the guess word list is all lowercase

            if current_letter in self.correct_word: # checks if the current letter is in the correct word
                if current_letter == self.correct_word[i]: # checks if the current letter is in the correct place
                    # updates the letter and key background color to green, if the current letter is in the correct word at the correct place
                    self.update_guesses_bg_color(i, current_letter, self.GREEN)
                    # sets the game result to "W" if non of the leters so far have been guessed uncorrectly (yellow or gray)
                    if not game_decided:
                        self.game_result = "W"
                else:
                    # updates the letter and key background color to yellow, and sets the game result to "" if any letters in the current guess are not in the correct word at the correct place
                    self.update_guesses_bg_color(i, current_letter, self.YELLOW)
                    self.game_result = ""
                    game_decided = True
            else:
                # updates the letter and key background color to grey, and clears the game result if any letters in the current guess are not in the correct word
                self.update_guesses_bg_color(i, current_letter, self.GREY) 
                self.game_result = ""
                game_decided = True
            
            pygame.display.update() # updates the screen after changing the background colors
        
        # increments the number of guesses and resets the current guess to prepare for the next guess
        self.guesses_count += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.current_textbox_x = self.TEXTBOX_START_X

        # checks if you have run out of guesses and not won the game, if so sets the game result to lose
        if self.guesses_count == self.MAX_GUESSES and self.game_result == "":
            self.game_result = "L"

    def reset(self):
        # Resets the game

        # fills the screen with white, to clear the previous game
        self.SCREEN.fill(self.BACKGROUND_COLOR)
        
        # resets the global variables
        self.correct_word = random.choice(WORDS) # picks a new random word from the word list
        self.correct_word_length = len(self.correct_word)
        self.guesses_count = 0
        self.guesses = [[] for _ in range(self.MAX_GUESSES)]
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = ""
        self.current_textbox_x = self.TEXTBOX_START_X
        self.current_textbox_y = self.TEXTBOX_START_Y
        self.score = 0 
        self.game_duration = 0

        # resets the objects
        self.textbox_grid_obj.draw_grid() # redraws the grid
        self.on_screen_keyboard_obj.reset_key_color() # resets the on screen keyboard key colors
        self.game_timer.activate_timer()

        pygame.display.update()

    def create_new_letter(self, letter):
        # creates a new textbox for the current letter, appends it to the gueeses and prints it to the screen

        self.current_guess_string += letter # adds a new letter to the current guess
        # updates the textbox y position for the next letter
        self.current_textbox_y = self.TEXTBOX_START_Y + self.guesses_count * (self.TEXTBOX_SIZE + self.TEXTBOX_Y_SPACING)
        # creates a new textbox and appends it to the current guess
        new_letter = Textbox(letter, self.GUESSED_LETTER_FONT, self.TEXTBOX_SIZE, self.BLACK, self.WHITE, self.LIGHT_GREY, self.current_textbox_x, self.current_textbox_y, self.SCREEN)
        # updates the textbox x position for the next letter
        self.current_textbox_x = self.TEXTBOX_START_X + len(self.current_guess_string) * (self.TEXTBOX_SIZE + self.TEXTBOX_X_SPACING)
        
        # appends the new textbox to the guesses and the current guess lists
        self.guesses[self.guesses_count].append(new_letter)
        self.current_guess.append(new_letter)

        # draws all the current guesses to the screen
        for guess in self.guesses:
            for letter in guess:
                letter.draw()

    def delete_letter(self):
        # deletes the last letter in the current guess and covers it with an empty textbox

        # covers up the last letter with an empty textbox, and removes it from the list
        self.guesses[self.guesses_count][-1].delete()
        self.guesses[self.guesses_count].pop()

        # removes the last letter from the current guess string and current guess list
        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()

        # updates the textbox x position for the next letter
        self.current_textbox_x = self.TEXTBOX_START_X + len(self.current_guess_string) * (self.TEXTBOX_SIZE + self.TEXTBOX_X_SPACING)

    def game_loop(self, game_runing):
        while game_runing:
            
            # starts timer and draws it on screen
            self.game_timer.draw()
            
            if self.return_button.draw(self.SCREEN):
                print("Return to Menu")
                self.reset()
                game_runing = False
                return # exit the game loop and return to the menu

            # On-screen keyboard events
            for keys in self.on_screen_keyboard_obj.key_button_list:
                button_clicked = keys.draw(self.SCREEN) # draws the button and checks if it was clicked
                
                # checks whitch button was clicked and updates the game accordingly
                if button_clicked == "ENT":
                    if self.game_result != "": # if the enter key is pressed, checks if the game is over, if so, resets the game
                        self.reset()
                    else:
                        # checks if the current guess is 1) the correct length and 2) in the word list, if so, runs the check guess function
                        if len(self.current_guess_string) == self.correct_word_length and self.current_guess_string.lower() in WORDS:
                            self.check_guess()
                            # pauses game timer and returns game time
                            if self.game_result != "":
                                self.game_duration = self.game_timer.stop_timer()
                            
                elif button_clicked == "DEL":
                    if len(self.current_guess_string) > 0: #checks if there are any letters in the current guess,. if so, deletes the last letter
                        self.delete_letter()
                else:
                    if str(button_clicked) in self.ALPHABET and self.game_result == "": # checks if the button clicked is in the alphabet
                        letter_pressed = button_clicked.upper()
                        if len(self.current_guess_string) < self.correct_word_length: # checks if the current guess is less than the length of the correct length, if so, runs the create new letter function,
                            self.create_new_letter(letter_pressed)

            # Keyboard events
            for event in pygame.event.get(): # checks for events (key presses, mouse clicks, etc.)
                if event.type == pygame.QUIT: # checks if the close button was pressed, if so quits the game
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN: # checks if a key was pressed
                    if event.key == pygame.K_RETURN: # if the enter key is pressed, checks if the game is over, if so, resets the game
                        if self.game_result != "":
                            self.reset()
                        else:
                            # checks if the current guess is 1) the correct length and 2) in the word list, if so, runs the check guess function
                            if len(self.current_guess_string) == self.correct_word_length and self.current_guess_string.lower() in WORDS:
                                self.check_guess()
                                # pauses game timer and returns game time
                                if self.game_result != "":
                                    self.game_duration = self.game_timer.stop_timer()
                                
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.current_guess_string) > 0: # checks if there are any letters in the current guess,. if so, deletes the last letter
                            self.delete_letter()
                    else:
                        key_pressed = event.unicode.upper() # converts the key pressed to uppercase
                        if key_pressed != "" and key_pressed in self.ALPHABET and self.game_result == "": # checks if the key pressed is in the alphabet
                            if len(self.current_guess_string) < self.correct_word_length: # checks if the current guess is less than the length of the correct length, if so, runs the create new letter function
                                self.create_new_letter(key_pressed)
            # if the game is over, draws the game results
            if self.game_result != "":
                # checks if the game result is W or L, if so, draws the game results 
                if self.game_result == "W":
                    game_results_obj = Game_Results(20, 20, self.GAME_RESULTS_FONT, self.BLACK, self.WHITE, "You won! =^)", str(self.score), "Press ENTER to Play Again!", self.correct_word)
                else:
                    game_results_obj = Game_Results(20, 20, self.GAME_RESULTS_FONT, self.BLACK, self.WHITE, "You Lost! =^(", str(self.score), "Press ENTER to Play Again!", self.correct_word)
                # draws the game results
                game_results_obj.draw_results(self.SCREEN)
                
            pygame.display.flip()
