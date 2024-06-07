import pygame

# initiates pygame session allowing pygame functions to be used.
pygame.init()

# CONSTANTS

LETTER_SIZE = 25
LETTER_BOX_SIZE = LETTER_SIZE * 2
LETTER_BOX_X_SPACING = LETTER_BOX_SIZE // 2
LETTER_BOX_Y_SPACING = LETTER_BOX_SIZE // 3

AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.ttf", LETTER_SIZE)
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]


# COLORS
WHITE = "FFFFFF"
BLACK = "000000"
GREY = "#787c7e"
OUTLINE = "#d3d6da"

selected_SCREEN = None
indicators_rect = None
starting_x = None
starting_y = None

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

class Indicator:
    def __init__(self, SCREEN, start_x, start_y, letter = None):
        # Initializes variables such as color, size, position, and letter.
        global selected_SCREEN, indicators_rect, starting_x, starting_y

        selected_SCREEN = SCREEN
        startig_x = start_x
        starting_y = start_y

        if letter != None:
            self.text = letter

        # interal variables
        self.rect = ((starting_x, starting_y), (LETTER_BOX_SIZE, LETTER_BOX_SIZE))
        indicators_rect = ((starting_x, starting_y), (len(ALPHABET[0]) * LETTER_BOX_SIZE, len(ALPHABET) * LETTER_BOX_SIZE))
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        global indicators_rect
        
        pygame.draw.rect(indicators_rect, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(LETTER_SIZE *2, LETTER_SIZE *2))
        indicators_rect.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def update(self, letter, color):
        # Updates the color of the indicator according to the guessed letter, and the input color.
        if self.text == letter.upper():
            self.bg_color = color
            self.draw()
    
    # @staticmethod
    def draw_indicators(self):
    # Drawing the indicators on the screen.
        global indicators, indicators_rect, starting_x, starting_y, selected_SCREEN

        pygame.draw.rect(selected_SCREEN, BLACK, indicators_rect)

        edge_buffer = 10
        indicator_x, indicator_y = starting_x + edge_buffer, starting_y + edge_buffer

        # creates indicators for each letter in ALPHABET.

        for i in range(len(ALPHABET)):
            for letter in ALPHABET[i]:
                new_indicator = Indicator(letter)
                indicators.append(new_indicator)
                new_indicator.draw()
                indicator_x += LETTER_BOX_X_SPACING

            indicator_y += LETTER_BOX_Y_SPACING

            if i == 0:
                indicator_x = starting_x + edge_buffer * 1.5
            elif i == 1:
                indicator_x = starting_x + edge_buffer * 2