import pygame

class Text:
    """
    A class for rendering and managing text in a Pygame application with optional text wrapping and background coloring.

    Attributes:
        text (str): The text to render.
        font (pygame.font.Font): The font used to render the text.
        x (int): The x-coordinate of the top-left corner of the text.
        y (int): The y-coordinate of the top-left corner of the text.
        max_width (int, optional): The maximum width for text wrapping. If None, no wrapping is applied.
        text_color (tuple, optional): The color of the text in RGB format. Default is (0, 0, 0) (black).
        bg_color (tuple, optional): The background color of the text in RGB format. If None, no background is drawn.
        center (bool, optional): Whether to center the text. Default is False.
    """

    def __init__(self, text, font, x, y, max_width=None, text_color=(0, 0, 0), bg_color=None, center=False):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.max_width = max_width
        self.text_color = text_color
        self.bg_color = bg_color
        self.center = center

        # Rendered text and dimensions
        self.rendered_text = None
        self.text_rect = None
        self.wrapped_text = None
        self.width = 0
        self.height = 0

        # Render text initially
        self._render_text()

    def _render_text(self):
        """
        Renders the text based on whether wrapping is required and calculates its dimensions.
        """
        if self.max_width is None:
            # Render single-line text
            self.rendered_text = self.font.render(self.text, True, self.text_color)
            self.text_rect = self.rendered_text.get_rect(topleft=(self.x, self.y))

            # Center text if needed
            if self.center:
                self.text_rect = self.rendered_text.get_rect(center=(self.x, self.y))

            self.width = self.rendered_text.get_width()
            self.height = self.rendered_text.get_height()
        else:
            # Render and wrap text if max_width is set
            self._wrap_text()
            self.line_count = len(self.wrapped_text)
            self.longest_line = max(self.wrapped_text, key=lambda line: line.get_width())
            self.width = self.longest_line.get_width()
            self.height = self.font.get_linesize() * self.line_count

    def _wrap_text(self):
        """
        Wraps the text into multiple lines based on the max_width.
        """
        words = self.text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            # Check if adding this word would exceed the max_width
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)
        # Render each line individually
        self.wrapped_text = [self.font.render(line.strip(), True, self.text_color) for line in lines]

    def draw(self, surface):
        """
        Draws the text on the given surface, handling both wrapped and single-line cases.

        Args:
            surface (pygame.Surface): The surface to draw the text on.
        """
        # Draw the background rectangle if bg_color is set
        self._draw_background(surface)

        if self.max_width is None:
            # Draw single-line text
            surface.blit(self.rendered_text, self.text_rect)
        else:
            # Draw wrapped text
            y_offset = 0
            for line in self.wrapped_text:
                surface.blit(line, (self.x, self.y + y_offset))
                y_offset += self.font.get_linesize()

    def _draw_background(self, surface):
        """
        Draws the background rectangle behind the text if bg_color is set.

        Args:
            surface (pygame.Surface): The surface to draw the background on.
        """
        if self.bg_color is not None:
            pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
