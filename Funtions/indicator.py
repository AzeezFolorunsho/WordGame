import pygame

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)

indicators = []

class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.text_pos = (self.x + ((square_size / 1.5) / 2), self.y + (square_size / 2.5))
        self.rect = (self.x, self.y, square_size / 1.5, square_size)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center = self.text_pos)
        SCREEN.blit(self.text_surface, self.text_rect)
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
        
        indicator_x = start_x - ((square_size * word_length) - LETTER_X_SPACING )/ word_length
        indicator_y = start_y + ((square_size * max_guesses) + (LETTER_Y_SPACING * (max_guesses - 1))) + (LETTER_Y_SPACING / 2)

        for i in range(3):
            for letter in ALPHABET[i]:
                new_indicator = Indicator(indicator_x, indicator_y, letter)
                indicators.append(new_indicator)
                new_indicator.draw()
                indicator_x += square_size - LETTER_X_SPACING * 2
            indicator_y += square_size + LETTER_X_SPACING * 2
            if i == 0:
                indicator_x = (start_x - ((square_size * word_length) - LETTER_X_SPACING )/ word_length) + (new_indicator.rect[2] / 2)
            elif i == 1:
                indicator_x = (start_x - ((square_size * word_length) - LETTER_X_SPACING )/ word_length) + (new_indicator.rect[2] * 1.6)