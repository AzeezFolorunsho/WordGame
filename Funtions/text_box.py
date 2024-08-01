import pygame

class Text_box:
    def __init__(self, text, font, square_size, text_color, bg_color, outline_color, x, y, screen, filled_outline_color):
        self.bg_color = bg_color
        self.text_color = text_color
        self.x = x
        self.y = y
        self.bg_rect = (self.x, self.y, square_size, square_size)
        self.text = text
        self.text_position = (self.x + (square_size / 2), self.y + (square_size / 2))
        self.text_surface = font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)
        self.square_size = square_size
        self.font = font
        self.screen = screen
        self.filled_outline_color = filled_outline_color
        self.outline_color = outline_color

    # Puts the letter and text on the screen at the desired positions.
    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(self.screen, self.filled_outline_color, self.bg_rect, 3)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    # Fills the letter's spot with the default square, emptying it.
    def delete(self):
        pygame.draw.rect(self.screen, "white", self.bg_rect)
        pygame.draw.rect(self.screen, self.outline_color, self.bg_rect, 3)
        pygame.display.update()