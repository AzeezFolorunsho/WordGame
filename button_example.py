import pygame
from Funtions import button

# Display window
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wordle+ Buttons")

# Load button images
classic_img = pygame.image.load("assets/classic_btn.png").convert_alpha()
hangman_img = pygame.image.load("assets/hangman_btn.png").convert_alpha()
crosswordle_img = pygame.image.load("assets/crosswordle_btn.png").convert_alpha()
vs_ai_img = pygame.image.load("assets/vs_ai_btn.png").convert_alpha()

# Button instances
classic_button = button.Button(100, 200, classic_img, 0.5)
hangman_button = button.Button(100, 400, hangman_img, 0.5)
crosswordle_button = button.Button(450, 200, crosswordle_img, 0.5)
vs_ai_button = button.Button(450, 400, vs_ai_img, 0.5)

# Game loop
run = True
while run:
    
    screen.fill((202, 228, 241))
    
    if classic_button.draw(screen):
        print("Classic")
    if hangman_button.draw(screen):
        print("Hangman")
    if crosswordle_button.draw(screen):
        print("Crosswordle")
    if vs_ai_button.draw(screen):
        print("Vs AI")
    
    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
    
pygame.quit()
