import pygame
import sys
from Funtions.buttons import Img_Button
from Funtions.text import Text
from WordleClassic import WordleClassic
from WordleHangman import WordleHangman
from WordleCrosswordle import play_crossword
from WordleVsAI import play_ai
from Funtions.settings import Settings  # Import the Settings class

# Load settings
settings = Settings('Local_Files\Settings.json')
screen_width = settings.get("General", {}).get("Screen Dimensions", {}).get("width", 1280)
screen_height = settings.get("General", {}).get("Screen Dimensions", {}).get("height", 720)
background_color = settings.get("General", {}).get("Background Color", "#72E2FF")
username = settings.get("User Profiles", {}).get("Username", "Player1")

# Pygame setup
pygame.init()

# Initialize screen for pygame
SCREEN = pygame.display.set_mode((screen_width, screen_height))
ICON = pygame.image.load("assets/wordle+logo.png")
pygame.display.set_icon(ICON)
pygame.display.set_caption("Wordle+")

# Fonts
WELCOME_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
USERNAME_FONT = pygame.font.SysFont('Comic Sans MS', 25)
TAGLINE_FONT = pygame.font.SysFont('Comic Sans MS', 20)
TEST_FONT = pygame.font.SysFont('Comic Sans MS', 35)

# Fill the screen with background color
SCREEN.fill(background_color)
pygame.display.update()

# CONSTANTS

# Game selection dimensions
STARTING_X = 100
STARTING_Y = (screen_height / 2) - 100
X_SPACING = 100

# Color
BLACK = "#000000"
WHITE = "#FFFFFF"

# Global Variables
current_x = STARTING_X
tagline_list = []

# Load button images
CLASSIC_IMG = pygame.image.load("assets/classic_btn.png").convert_alpha()
HANGMAN_IMG = pygame.image.load("assets/hangman_btn.png").convert_alpha()
CROSSWORDLE_IMG = pygame.image.load("assets/crosswordle_btn.png").convert_alpha()
VS_AI_IMG = pygame.image.load("assets/vs_ai_btn.png").convert_alpha()
SETTINGS_IMG = pygame.image.load("assets/settings_icon.png").convert_alpha()

# Button instances
classic_button = Img_Button(0, 0, CLASSIC_IMG, 0.5)
hangman_button = Img_Button(0, 0, HANGMAN_IMG, 0.5)
crosswordle_button = Img_Button(0, 0, CROSSWORDLE_IMG, 0.5)
vs_ai_button = Img_Button(0, 0, VS_AI_IMG, 0.5)
settings_button = Img_Button(screen_width - 80 , 20 , SETTINGS_IMG, 0.9)

# Functions and logic
def game_selector(button, tagline_message):
    global current_x, tagline_list

    button.set_x_and_y(current_x, STARTING_Y)
    tagline_text = Text(tagline_message, TAGLINE_FONT, BLACK, current_x, STARTING_Y + button.rect.height, button.rect.width)
    tagline_list.append(tagline_text)
    current_x += button.rect.width + X_SPACING

# Set up game selectors
classic_game_selector = game_selector(classic_button, "Guess the word before you run out of tries!")
hangman__game_selector = game_selector(hangman_button, "Guess the word before the man hangs!")
crosswordle__game_selector = game_selector(crosswordle_button, "Try your best to guess the word, don't get crossed up.")
vs_ai_game_selector = game_selector(vs_ai_button, "Prepare for the coming AI takeover, practice your skill against your future oppressors!")

# Display welcome message
welcome_message_text = Text("Welcome to Wordle+!", WELCOME_FONT, BLACK, (screen_width / 2) - (499 / 2), 50, screen_width)
username_text = Text(username, USERNAME_FONT, BLACK, (screen_width / 2), 150, screen_width)

pygame.display.update()

# Game loop
while True:
    # Draw welcome message
    welcome_message_text.draw_line(SCREEN)

    # Draw username
    username_text.draw_line(SCREEN)

    # Draw taglines
    for tagline in tagline_list:
        tagline.draw_wrapped(SCREEN)

    # Draw buttons
    if classic_button.draw(SCREEN):
        print("Classic")
        game = WordleClassic(settings)
        game.game_loop(True)
        SCREEN.fill(background_color)

    if hangman_button.draw(SCREEN):
        print("Hangman")
        game = WordleHangman(settings)
        game.game_loop(True)
        SCREEN.fill(background_color)

    if crosswordle_button.draw(SCREEN):
        print("Crosswordle")
        play_crossword()
        SCREEN.fill(background_color)

    if vs_ai_button.draw(SCREEN):
        print("Vs AI")
        play_ai()
        SCREEN.fill(background_color)

    if settings_button.draw(SCREEN):
        print("Settings")
        SCREEN.fill(background_color)

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
