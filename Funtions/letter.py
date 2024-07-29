import pygame

class Letter:
    def __init__(self, text, bg_position, square_size, GUESSED_LETTER_FONT, SCREEN, FILLED_OUTLINE):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (self.bg_x, self.bg_y, square_size, square_size)
        self.text = text
        self.text_position = (self.bg_x + (square_size / 2), self.bg_y + (square_size / 2))
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)
        self.square_size = square_size
        self.GUESSED_LETTER_FONT = GUESSED_LETTER_FONT
        self.SCREEN = SCREEN
        self.FILLED_OUTLINE = FILLED_OUTLINE
        self.OUTLINE = "#d3d6da"

    # Puts the letter and text on the screen at the desired positions.
    def draw(self):
        pygame.draw.rect(self.SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(self.SCREEN, self.FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = self.GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    # Fills the letter's spot with the default square, emptying it.
    def delete(self):
        pygame.draw.rect(self.SCREEN, "white", self.bg_rect)
        pygame.draw.rect(self.SCREEN, self.OUTLINE, self.bg_rect, 3)
        pygame.display.update()
