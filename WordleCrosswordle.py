import pygame

def play_crossword():
    # pygame setup
    pygame.init()

    WIDTH, HEIGHT = 1280, 720

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("red")
    pygame.display.update()

    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()