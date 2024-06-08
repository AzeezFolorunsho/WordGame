import pygame

# pygame setup
pygame.init()

# CONSTANTS

LETTER_SIZE = 25
LETTER_BOX_SIZE = LETTER_SIZE * 2
LETTER_BOX_X_SPACING = LETTER_BOX_SIZE // 2
LETTER_BOX_Y_SPACING = LETTER_BOX_SIZE // 3

AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.ttf", LETTER_SIZE)
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]


# COLORS
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#787c7e"
OUTLINE = "#d3d6da"

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

class Indicator:
    def __init__(self, SCREEN, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.SCREEN = SCREEN
        self.x = x
        self.y = y
        self.text = letter
        self.rect = ((self.x, self.y), (LETTER_BOX_SIZE, LETTER_BOX_SIZE))
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.        
        pygame.draw.rect(self.SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (LETTER_BOX_SIZE * 1.5), self.y + (LETTER_BOX_SIZE * 1.5)))
        self.SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()


    def update(self, letter, color):
        # Updates the color of the indicator according to the guessed letter, and the input color.
        if self.text == letter.upper():
            self.bg_color = color
            self.draw()
    
    @staticmethod
    def draw_indicators(Screen, start_x, start_y):
    # Drawing the indicators on the screen.

        # experiement
        indicators_rect = ((start_x, start_y), (len(ALPHABET[0]) * LETTER_BOX_SIZE, len(ALPHABET) * LETTER_BOX_SIZE))

        pygame.draw.rect(Screen, BLACK, indicators_rect)

        edge_buffer = 10
        indicator_x, indicator_y = start_x + edge_buffer, start_y + edge_buffer

        # creates indicators for each letter in ALPHABET.

        for i in range(len(ALPHABET)):
            for letter in ALPHABET[i]:
                new_indicator = Indicator(Screen, indicator_x, indicator_y, letter)
                indicators.append(new_indicator)
                new_indicator.draw()
                indicator_x += LETTER_BOX_X_SPACING

            indicator_y += LETTER_BOX_Y_SPACING

            if i == 0:
                indicator_x = start_x + edge_buffer * 1.5
            elif i == 1:
                indicator_x = start_x + edge_buffer * 2