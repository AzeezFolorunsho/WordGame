import pygame

class Indication:
    def __init__(self, indicators, guesses):
        self.indicators = indicators
        self.guesses = guesses

    def update(self, letter, updated_bg_color):
        self.letter = letter
        self.updated_bg_color = updated_bg_color

        for indicator in self.indicators:
            indicator.update(letter, updated_bg_color)

        #self.indicator.update(self.letter, self.updated_bg_color)

        for guess in self.guesses:
            for letters in guess:
                if letters.text == letter:
                    letters.update(letter, updated_bg_color)

        pygame.display.update()