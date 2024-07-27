import pygame

OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
GUESSED_LETTER_FONT = pygame.font.Font("../assets/FreeSansBold.otf", 50)

# create individual letters that can be added to a word guess in the game.
class Letter:
    def __init__(self, screen, text, bg_position, square_size):
        # Initializes all the variables, including text, color, position, size, etc.
        self.screen = screen
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (self.bg_x, self.bg_y, square_size, square_size)
        self.text = text
        self.text_position = (self.bg_x + (square_size / 2), self.bg_y + (square_size / 2))
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center = self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(self.screen, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(self.screen, "white", self.bg_rect)
        pygame.draw.rect(self.screen, OUTLINE, self.bg_rect, 3)
        pygame.display.update()