import pygame
import sys
from Funtions import button
from Funtions import text
from WorldeClasicMain import play_classic
from WordleCrossword import play_crossword
from WordleHangman import play_hangman
from WordleVsAI import play_ai

# pygame setup
pygame.init()

# CONSTANTS

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# initiates screen for pygame
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set icon and caption
ICON = pygame.image.load("assets/wordle+logo.png")
pygame.display.set_icon(ICON)
pygame.display.set_caption("Wordle+")

# Fonts
welcome_font = pygame.font.SysFont('Comic Sans MS', 50)
tagline_font = pygame.font.SysFont('Comic Sans MS', 20)

# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"
BACKGROUND_COLOR = "#72E2FF"
TAGLINE_COLOR = BLACK

# fill the screen with a color to wipe away anything from last frame
SCREEN.fill(BACKGROUND_COLOR)

# Update the display
pygame.display.update()

# Global Variables

# starting x and y for game buttons
starting_x = 100
starting_y = (SCREEN_HEIGHT / 2) - 100

# x spacing for game buttons
x_spacing = 100

# Load button images
classic_img = pygame.image.load("assets/classic_btn.png").convert_alpha()
hangman_img = pygame.image.load("assets/hangman_btn.png").convert_alpha()
crosswordle_img = pygame.image.load("assets/crosswordle_btn.png").convert_alpha()
vs_ai_img = pygame.image.load("assets/vs_ai_btn.png").convert_alpha()

# Button instances
classic_button = button.Button(0, 0, classic_img, 0.5)
hangman_button = button.Button(0, 0, hangman_img, 0.5)
crosswordle_button = button.Button(0, 0, crosswordle_img, 0.5)
vs_ai_button = button.Button(0, 0, vs_ai_img, 0.5)

# Functions and logic

def game_selector(button, tagline_message):
    global starting_x

    # changes button position to be in aligment with other buttons
    button.set_xand_y(starting_x, starting_y)

    # prints tagline message under button
    tagline_text = text.Text(tagline_message, tagline_font, TAGLINE_COLOR, starting_x, starting_y + button.rect.height, button.rect.width)
    tagline_text.draw_wrapped(SCREEN)

    # changes position for the next game selector
    starting_x += button.rect.width + x_spacing

classic_game_selector = game_selector(classic_button, "Guess the word, before you run out of tries!")
hangman_game_selector = game_selector(hangman_button, "Guess the word before the man hangs!")
crosswordle_game_selector = game_selector(crosswordle_button, "Try your best to guess the word, don't get crossed up.")
vs_ai_game_selector = game_selector(vs_ai_button, "Prepare for the coming AI takeover, practice your skill against your future oppressors!")

welcome_message = text.Text("Welcome to Wordle+!", welcome_font, WHITE, (SCREEN_WIDTH / 2) - (499 / 2), 50, SCREEN_WIDTH)
welcome_message.draw_line(SCREEN)

pygame.display.update()

# Game loop

while True:

    if classic_button.draw(SCREEN):
        print("Classic")
        play_classic()
    if hangman_button.draw(SCREEN):
        print("Hangman")
        play_crossword()
    if crosswordle_button.draw(SCREEN):
        print("Crosswordle")
        play_hangman()
    if vs_ai_button.draw(SCREEN):
        print("Vs AI")
        play_ai()

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
