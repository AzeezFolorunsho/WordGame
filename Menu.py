import pygame
from Funtions import button

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
font = pygame.font.SysFont('Comic Sans MS', 30)

# Colors
BACKGROUND_COLOR = "#72E2FF"
BLACK = "#000000"
TAGLINE_COLOR = BLACK

# fill the screen with a color to wipe away anything from last frame
SCREEN.fill(BACKGROUND_COLOR)

# Update the display
pygame.display.update()

# Gobal Variables

# starting x and y for game buttons
starting_x = 150
starting_y = SCREEN_HEIGHT / 2

# x spacing for game buttons
x_spacing = 150

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
    button.x = starting_x
    button.y = starting_y

    # prints tagline message under button
    draw_text(tagline_message, font, TAGLINE_COLOR, SCREEN, starting_x, starting_y + button.rect.height)

    # changes position for the next game selector
    starting_x += button.rect.width + x_spacing

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

classic_game_selector = game_selector(classic_button, "Classic")
hangman_game_selector = game_selector(hangman_button, "Hangman")
crosswordle_game_selector = game_selector(crosswordle_button, "Crosswordle")
vs_ai_game_selector = game_selector(vs_ai_button, "Vs AI")

draw_text("WELCOME TO WORDLE+", font, BLACK, SCREEN, (SCREEN_WIDTH/2) - 20, 50)


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

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
