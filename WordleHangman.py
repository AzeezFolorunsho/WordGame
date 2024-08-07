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

class WordleHangman:
    def __init__(self):
        # Initialize Constants and pygame
        self.setup_constants()
        self.setup_pygame()
        
        ################################### Global Variables (will be accesed and changed througout the game) ###################################
        
        self.current_guess = [] # tracks the current guesses
        self.incorect_guesses = 0 # tracks the number of incorrect guesses
        
        self.game_result = "" # tracks the game result "W" = Win, "L" = Loss, "" = undesided
        
        self.score = 100 # tracks the score, will be set to a prpber calculation later
        
        # sets the current textbox position
        self.correct_word_textbox_current_x = self.CORRECT_WORD_TEXTBOX_START_X

        # sets the correct word
        self.correct_word = "coder" # hardcoded for testing, will be replaced with: random.choice(WORDS)
        self.correct_word_length = len(self.correct_word)
        self.correct_word_textbox_list = self.set_correct_word_textbox_list()

        # Initialize game objects
        
        # Text box grid for the correct word
        self.correct_word_textbox_grid_obj = Textbox_grid(
            self.SCREEN, self.TEXTBOX_SIZE, 1, 
            self.correct_word_length, self.CORRECT_WORD_TEXTBOX_X_SPACING, 
            self.CORRECT_WORD_TEXTBOX_Y_SPACING, self.CORRECT_WORD_TEXTBOX_START_X, 
            self.CORRECT_WORD_TEXTBOX_START_Y, self.LIGHT_GREY, self.WHITE
        )
        
        # Text box grid offset
        self.offset = self.CORRECT_WORD_TEXTBOX_START_X + (self.correct_word_textbox_grid_obj.columns * 
                                              (self.correct_word_textbox_grid_obj.square_size + 
                                               self.correct_word_textbox_grid_obj.x_spacing))
        
        # guess textbox grid dimensions
        self.CURRENT_GUESS_TEXTBOX_X = self.offset + self.TEXTBOX_SIZE
        self.CURRENT_GUESS_TEXTBOX_Y = self.CORRECT_WORD_TEXTBOX_START_Y - self.TEXTBOX_SIZE
        # sets the current guess textbox grid
        self.current_guess_textbox_grid_obj = Textbox_grid(
            self.SCREEN, self.TEXTBOX_SIZE, 1, 
            1, 0, 0, self.CURRENT_GUESS_TEXTBOX_X, 
            self.CURRENT_GUESS_TEXTBOX_Y, self.LIGHT_GREY, self.WHITE
        )

        # Draws the grid the first time
        self.correct_word_textbox_grid_obj.draw_underlined_grid()
        self.current_guess_textbox_grid_obj.draw_grid()

        # sets the on screen Keyboard
        self.on_screen_keyboard_obj = On_Screen_Keyboard(
            self.KEYBOARD_START_X, self.KEYBOARD_START_Y, 
            self.KEYBOARD_X_SPACING, self.KEYBOARD_Y_SPACING, 
            self.KEYBOARD_WIDTH, self.KEYBOARD_HEIGHT, 
            self.ON_SCREEN_KEYBOARD_FONT, self.WHITE, 
            self.LIGHT_GREY, self.MEDIUM_GREY
        )

        # sets the return button
        self.return_button = Text_Button(
            "Return", self.ON_SCREEN_KEYBOARD_FONT, 
            self.WHITE, self.BLACK, self.LIGHT_GREY, 
            self.SCREEN_WIDTH - 140, 27, 110, 45
        )

        # sets the temporary guides
        self.guide = Guide(self.SCREEN)
        self.guide.draw_guides_thirds(self.BLACK)
        self.guide.draw_guides_cross(self.RED)

        # Importing Hangman images and storing as a list
        self.hangman_images = [pygame.image.load(f"assets/hangman_images/hangman{i}.png") for i in range(7)]
        self.current_hangman_image = self.hangman_images[0]

        # Draw the initial hangman image on the screen
        # self.SCREEN.blit(self.current_hangman_image, (410, 10))  
        self.image_swap()
        pygame.display.update()

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
        self.MAX_GUESSES = 7
        # Textbox Dimensions
        self.TEXTBOX_SIZE = 62.4
        self.CORRECT_WORD_TEXTBOX_START_X = 468
        self.CORRECT_WORD_TEXTBOX_START_Y = self.SCREEN_HEIGHT/2
        self.CORRECT_WORD_TEXTBOX_X_SPACING = 8
        self.CORRECT_WORD_TEXTBOX_Y_SPACING = 20
        # hangman image dimensions
        self.HANGMAN_IMAGE_X = 410
        self.HANGMAN_IMAGE_Y = 10
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

    def setup_pygame(self):
        # initialize pygame, screen, and icon
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # set icon and caption
        self.icon = pygame.image.load("assets/wordle+logo.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Wordle+ Hangman")
        # fills screen with white
        self.SCREEN.fill(self.BACKGROUND_COLOR)

    def set_correct_word_textbox_list(self):
        self.correct_word_letters_temp = []
        for letter in self.correct_word:
            self.correct_word_letters_temp.append(Textbox(letter.upper(), self.GUESSED_LETTER_FONT, 
                                                          self.TEXTBOX_SIZE, self.BLACK, self.WHITE, 
                                                          self.LIGHT_GREY, self.correct_word_textbox_current_x, 
                                                          self.CORRECT_WORD_TEXTBOX_START_Y, self.SCREEN
                                                          ))
            self.correct_word_textbox_current_x += self.TEXTBOX_SIZE + self.CORRECT_WORD_TEXTBOX_X_SPACING
        return self.correct_word_letters_temp

    def update_guesses_bg_color(self, index, letter, color):
        # updates the background color of a given textbox and the on screen keyboard key of the same letter to the given color
        if self.IS_INDICATING:
            self.on_screen_keyboard_obj.update_key_color(letter, color)
            self.correct_word_textbox_list[index].update_bg_color(letter, color)

    def check_guess(self):
        letter_in_correct_word = False # used to determine if the current guess is in the correct word
        game_is_won = False # used to determine if the game has been won

        # checks if the current guess is in the correct word
        for i in range(len(self.correct_word)):
            
            current_letter = self.current_guess[-1].text.lower() # converts the current letter to lowercase beacuse the guess word list is all lowercase

            if self.correct_word[i] == current_letter: # checks if the current letter is in the correct word
                self.update_guesses_bg_color(i, current_letter, self.GREEN)
                self.correct_word_textbox_list[i].draw()
                letter_in_correct_word = True

        if letter_in_correct_word == False:    
            self.on_screen_keyboard_obj.update_key_color(current_letter, self.GREY)
            
        if letter_in_correct_word == False: # if the current guess is not in the correct word
            self.incorect_guesses += 1
            self.image_swap()
            # RUN HANGMAN
            
        pygame.display.update() # updates the screen after changing the background colors
        
        self.current_guess[-1].delete()
        # increments the number of guesses and resets the current guess to prepare for the next guess
        self.current_guess = []
        
        for textbox in self.correct_word_textbox_list:
            if textbox.bg_color == self.GREEN:
                game_is_won = True
            else:
                game_is_won = False
                break
        
        if game_is_won == True:
            self.game_result = "W"

        # checks if you have run out of guesses and not won the game, if so sets the game result to lose
        if self.incorect_guesses == self.MAX_GUESSES and game_is_won == False:
            self.game_result = "L"

    def reset(self):
        # Resets the game

        # fills the screen with white, to clear the previous game
        self.SCREEN.fill(self.BACKGROUND_COLOR)
        
        # resets the global variables
        self.correct_word = random.choice(WORDS) # picks a new random word from the word list
        self.correct_word_length = len(self.correct_word)
        self.current_guess = []
        self.game_result = ""
        self.score = 0 
        self.incorect_guesses = 0

        # sets the correct word textbox list
        self.correct_word_textbox_list = self.set_correct_word_textbox_list()

        # resets the objects
        self.correct_word_textbox_grid_obj.draw_underlined_grid() # redraws the grid
        self.on_screen_keyboard_obj.reset_key_color() # resets the on screen keyboard key colors
        self.current_guess_textbox_grid_obj.draw_grid()

        pygame.display.update()

    def create_new_letter(self, letter):
        # creates a new textbox and appends it to the current guess
        new_letter = Textbox(letter, self.GUESSED_LETTER_FONT, self.TEXTBOX_SIZE, self.BLACK, self.WHITE, self.LIGHT_GREY, self.CURRENT_GUESS_TEXTBOX_X, self.CURRENT_GUESS_TEXTBOX_Y, self.SCREEN)
        # appends the new textbox to the current guess lists
        self.current_guess.append(new_letter)
        # draws the new textbox
        self.current_guess[-1].draw()

    def delete_letter(self):
        # covers up the last letter with an empty textbox, and removes it from the list
        self.current_guess[-1].delete()
        self.current_guess.pop()

    def image_swap(self):
        self.current_hangman_image = self.hangman_images[self.incorect_guesses]
        self.SCREEN.blit(self.current_hangman_image, (self.HANGMAN_IMAGE_X, self.HANGMAN_IMAGE_Y))
        pygame.display.update()

    def game_loop(self, game_runing):
        while game_runing:
            if self.return_button.draw(self.SCREEN):
                print("Return to Menu")
                self.reset()
                game_runing = False
                return  # exit the game loop and return to the menu

            # On-screen keyboard events
            for keys in self.on_screen_keyboard_obj.key_button_list:
                button_clicked = keys.draw(self.SCREEN) # draws the button and checks if it was clicked
                
                # checks which button was clicked and updates the game accordingly
                if button_clicked == "ENT":
                    if self.game_result != "": # if the enter key is pressed, checks if the game is over, if so, resets the game
                        self.reset()
                    else:
                        if len(self.current_guess) > 0:
                            self.check_guess()
                elif button_clicked == "DEL":
                    if len(self.current_guess) > 0: #checks if there are any letters in the current guess,. if so, deletes the last letter
                        self.delete_letter()
                else:
                    if str(button_clicked) in self.ALPHABET: # checks if the button clicked is in the alphabet
                        letter_pressed = button_clicked.upper()
                        if len(self.current_guess) < 1: # checks if the current guess is less than 2
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
                            if len(self.current_guess) > 0:
                                self.check_guess()
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.current_guess) > 0: # checks if there are any letters in the current guess,. if so, deletes the last letter
                            self.delete_letter()
                    else:
                        key_pressed = event.unicode.upper() # converts the key pressed to uppercase
                        if key_pressed in self.ALPHABET and key_pressed != "": # checks if the key pressed is in the alphabet
                            if len(self.current_guess) < 1: # checks if the current guess is less than the length of the correct length, if so, runs the create new letter function
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
