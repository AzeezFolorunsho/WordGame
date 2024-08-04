import pygame
import sys
from Funtions import buttons
from Funtions import text
from Funtions import on_screen_keyboard
from Funtions import game_results


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
WELCOME_FONT = pygame.font.SysFont('Comic Sans MS', 50)
TAGLINE_FONT = pygame.font.SysFont('Comic Sans MS', 20)

test_font = pygame.font.SysFont('Comic Sans MS', 35)


# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"
GREY = "#787c7e"
RED = "#FF0000"
BACKGROUND_COLOR = "#72E2FF"

# fill the screen with a color to wipe away anything from last frame
SCREEN.fill(BACKGROUND_COLOR)

# Update the display
pygame.display.update()

# Gobal Variables

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
classic_button = buttons.Img_Button(0, 0, classic_img, 0.5)
hangman_button = buttons.Img_Button(0, 0, hangman_img, 0.5)
crosswordle_button = buttons.Img_Button(0, 0, crosswordle_img, 0.5)
vs_ai_button = buttons.Img_Button(0, 0, vs_ai_img, 0.5)

# tempoary tests:

# textbutton example
text_button = buttons.Text_Button("text", TAGLINE_FONT, BLACK, GREY, SCREEN_WIDTH/2, 200, 100, 50)
# text_button.set_x_and_y(SCREEN_WIDTH/5, 200)
text_button.x = SCREEN_WIDTH/5

# on screen keyboard test
keyboard = on_screen_keyboard.On_Screen_Keyboard(SCREEN_WIDTH / 3.3, SCREEN_HEIGHT / 1.47, 10, 20, 62 / 1.5, 62, test_font, WHITE, GREY)

# game results test
results = game_results.Game_Results(0, 0, test_font, BLACK, RED, "You won! nice job", "100", "Press enter to play again", "cat", "Dolphin", "Tripod", "Oragnesy")

# Functions and logic

def game_selector(button, tagline_message):
    global starting_x

    # changes button position to be in aligment with other buttons
    button.set_x_and_y(starting_x, starting_y)

    # prints tagline message under button
    tagline_text = text.Text(tagline_message, TAGLINE_FONT, BLACK, starting_x, starting_y + button.rect.height, button.rect.width)
    tagline_text.draw_wrapped(SCREEN)

    # changes position for the next game selector
    starting_x += button.rect.width + x_spacing

classic_game_selector = game_selector(classic_button, "Guess the word, before you run out of tries!")
hangman_game_selector = game_selector(hangman_button, "Guess the word before the man hangs!")
crosswordle_game_selector = game_selector(crosswordle_button, "Try your best to guess the word, don't get crossed up.")
vs_ai_game_selector = game_selector(vs_ai_button, "Prepare for the coming AI takeover, practice your skill against your future oppressors!")

welcome_message = text.Text("Welcome to Wordle+!", WELCOME_FONT, WHITE, (SCREEN_WIDTH / 2) - (499 / 2), 50, SCREEN_WIDTH)
welcome_message.draw_line(SCREEN)

pygame.display.update()

# Game loop

while True:

    if classic_button.draw(SCREEN):
        print("Classic")
    if hangman_button.draw(SCREEN):
        print("Hangman")
    if crosswordle_button.draw(SCREEN):
        print("Crosswordle")
    if vs_ai_button.draw(SCREEN):
        print("Vs AI")
    # if text_button.draw(SCREEN):
    #     print("text")
    if keyboard.draw(SCREEN) == "Q":
        print("DELETE")
    
    # results.draw_results(SCREEN)

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()