import pygame

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)

indicators = []

class Indicator:
    def __init__(self, start_x, start_y, size, x_spacing, y_spacing, SCREEN):
        # Initializes variables such as color, size, position, and letter.
        self.x = start_x
        self.y = start_y
        self.size = size
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.SCREEN = SCREEN
        # self.text_pos = (self.x + ((size * 0.5) / 2), self.y + (size / 2.5))
        self.rect = (self.x, self.y, size / 1.5, size)
        self.bg_color = "#d3d6da"

    def draw(self, text, x, y):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(self.SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center = self.text_pos)
        self.SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def update(self, letter, color):
        # Updates the color of the indicator according to the guessed letter, and the input color.
        if self.text == letter.upper():
            self.bg_color = color
            self.draw()
    
    @staticmethod
    def draw_indicators():
    # Drawing the indicators on the screen.
        global indicators
        
        indicator_x = start_x - ((size * word_length) - self.LETTER_X_SPACING )/ word_length
        indicator_y = start_y + ((size * max_guesses) + (self.LETTER_Y_SPACING * (max_guesses - 1))) + (self.LETTER_Y_SPACING / 2)

        for i in range(3):
            for letter in ALPHABET[i]:
                new_indicator = Indicator(indicator_x, indicator_y, letter)
                indicators.append(new_indicator)
                new_indicator.draw()
                indicator_x += size - self.LETTER_X_SPACING * 2
            indicator_y += size + self.LETTER_X_SPACING * 2
            if i == 0:
                indicator_x = (start_x - ((size * word_length) - self.LETTER_X_SPACING )/ word_length) + (new_indicator.rect[2] / 2)
            elif i == 1:
                indicator_x = (start_x - ((size * word_length) - self.LETTER_X_SPACING )/ word_length) + (new_indicator.rect[2] * 1.6)