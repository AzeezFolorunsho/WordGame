import pygame

class Textbox:
    """
    A class for rendering and managing a single textbox with text in a Pygame application.

    Attributes:
        text (str): The text to display inside the textbox.
        font (pygame.font.Font): The font used to render the text.
        square_size (int): The size of the square textbox.
        text_color (tuple): The color of the text.
        bg_color (tuple): The background color of the textbox.
        outline_color (tuple): The color of the textbox outline.
        x (int): The x-coordinate of the top-left corner of the textbox.
        y (int): The y-coordinate of the top-left corner of the textbox.
        screen (pygame.Surface): The Pygame surface to draw the textbox on.
    """

    def __init__(self, text, font, square_size, text_color, bg_color, outline_color, x, y, screen):
        self.text = text
        self.font = font
        self.square_size = square_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.outline_color = outline_color
        self.x = x
        self.y = y
        self.screen = screen

        self.bg_rect = pygame.Rect(self.x, self.y, self.square_size, self.square_size)
        self.text_position = (self.x + self.square_size / 2, self.y + self.square_size / 2)

    def draw_empty_box(self):
        """
        Draws an empty box on the screen.
        """
        pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
        pygame.draw.rect(self.screen, self.outline_color, self.bg_rect, 3)

    def draw(self):
        """
        Draws the textbox with text on the screen.
        """
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.text_position)
        self.draw_empty_box()
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def delete(self):
        """
        Clears the textbox by drawing an empty box.
        """
        self.draw_empty_box()
        pygame.display.update()

    def update_bg_color(self, letter, color):
        """
        Updates the background color of the textbox if the letter matches.

        Args:
            letter (str): The letter to check.
            color (tuple): The new background color to apply.
        """
        if self.text.upper() == letter.upper():
            self.text_color = (255, 255, 255)  # White
            self.bg_color = color
            self.outline_color = color
            self.draw()
