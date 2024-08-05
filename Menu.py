import pygame
import sys
from Funtions.buttons import Img_Button
from Funtions.text import Text
from WordleClassic import WordleClassic
from WordleHangman import WordleHangman
from WordleCrosswordle import play_crossword
from WordleVsAI import play_ai

# Pygame setup
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
BLACK = "#000000"
WHITE = "#FFFFFF"
GREY = "#787c7e"
RED = "#FF0000"
BACKGROUND_COLOR = "#72E2FF"

# Initialize screen for pygame
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ICON = pygame.image.load("assets/wordle+logo.png")
pygame.display.set_icon(ICON)
pygame.display.set_caption("Wordle+")

# Fonts
WELCOME_FONT = pygame.font.SysFont('Comic Sans MS', 50)
TAGLINE_FONT = pygame.font.SysFont('Comic Sans MS', 20)
TEST_FONT = pygame.font.SysFont('Comic Sans MS', 35)

# Fill the screen with background color
SCREEN.fill(BACKGROUND_COLOR)
pygame.display.update()

# Global Variables
STARTING_X = 100
STARTING_Y = (SCREEN_HEIGHT / 2) - 100
X_SPACING = 100

# Load button images
CLASSIC_IMG = pygame.image.load("assets/classic_btn.png").convert_alpha()
HANGMAN_IMG = pygame.image.load("assets/hangman_btn.png").convert_alpha()
CROSSWORDLE_IMG = pygame.image.load("assets/crosswordle_btn.png").convert_alpha()
VS_AI_IMG = pygame.image.load("assets/vs_ai_btn.png").convert_alpha()
settings_img = pygame.image.load("assets/settings_icon.png").convert_alpha()

# Button instances
classic_button = Img_Button(0, 0, CLASSIC_IMG, 0.5)
hangman_button = Img_Button(0, 0, HANGMAN_IMG, 0.5)
crosswordle_button = Img_Button(0, 0, CROSSWORDLE_IMG, 0.5)
vs_ai_button = Img_Button(0, 0, VS_AI_IMG, 0.5)
settings_button = Img_Button(SCREEN_WIDTH - 80 , 20 , settings_img, 0.9)

# Functions and logic
def game_selector(button, tagline_message, start_x):
    button.set_x_and_y(start_x, STARTING_Y)
    tagline_text = Text(tagline_message, TAGLINE_FONT, BLACK, start_x, STARTING_Y + button.rect.height, button.rect.width)
    tagline_text.draw_wrapped(SCREEN)
    return start_x + button.rect.width + X_SPACING

# Set up game selectors
STARTING_X = game_selector(classic_button, "Guess the word before you run out of tries!", STARTING_X)
STARTING_X = game_selector(hangman_button, "Guess the word before the man hangs!", STARTING_X)
STARTING_X = game_selector(crosswordle_button, "Try your best to guess the word, don't get crossed up.", STARTING_X)
STARTING_X = game_selector(vs_ai_button, "Prepare for the coming AI takeover, practice your skill against your future oppressors!", STARTING_X)

# Display welcome message
welcome_message = Text("Welcome to Wordle+!", WELCOME_FONT, WHITE, (SCREEN_WIDTH / 2) - (499 / 2), 50, SCREEN_WIDTH)

pygame.display.update()

# Game loop
while True:
    # Draw welcome message
    welcome_message.draw_line(SCREEN)
    # Draw buttons
    if classic_button.draw(SCREEN):
        print("Classic")
        game = WordleClassic()
        game.game_loop(True)

    if hangman_button.draw(SCREEN):
        print("Hangman")
        game = WordleHangman()
        game.game_loop(True)
    if crosswordle_button.draw(SCREEN):
        print("Crosswordle")
        play_crossword()
    if vs_ai_button.draw(SCREEN):
        print("Vs AI")
        play_ai()
    if settings_button.draw(SCREEN):
        print("Settings")

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
