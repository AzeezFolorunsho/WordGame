import pygame

class Text_box:
    def __init__(self, text, font, square_size, text_color, bg_color, outline_color, x, y, screen):
        self.text = text
        self.font = font
        self.square_size = square_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.outline_color = outline_color
        self.x = x
        self.y = y
        self.bg_rect = (self.x, self.y, self.square_size, self.square_size)
        self.text_position = (self.x + (self.square_size / 2), self.y + (self.square_size / 2))
        self.screen = screen

    def draw_empty_box(self):
        pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
        pygame.draw.rect(self.screen, self.outline_color, self.bg_rect, 3)

    # Puts the letter and text on the screen at the desired positions.
    def draw(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

        self.draw_empty_box()
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    # Fills the letter's spot with the default square, emptying it.
    def delete(self):
        self.draw_empty_box()
        pygame.display.update()

    def update(self, letter, color):
        # Updates the color of the indicator according to the guessed letter, and the input color.
        if self.text == letter.upper():
            self.text_color = "#FFFFFF"
            self.bg_color = color
            self.outline_color = color
            self.draw()