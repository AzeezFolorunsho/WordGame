import pygame

class TextboxGrid:
    """
    Class for managing a grid of textboxes for a game interface.

    Attributes:
        screen (pygame.Surface): The Pygame surface to draw the grid on.
        square_size (int): The size of each square in the grid.
        rows (int): Number of rows in the grid.
        columns (int): Number of columns in the grid.
        x_spacing (int): Horizontal spacing between squares.
        y_spacing (int): Vertical spacing between squares.
        start_x (int): X-coordinate for the starting position of the grid.
        start_y (int): Y-coordinate for the starting position of the grid.
        outline_color (tuple): Color for the outline of the squares.
        bg_color (tuple): Background color for the squares.
    """

    BLACK = (0, 0, 0)

    def __init__(self, screen, square_size, rows, columns, x_spacing, y_spacing, start_x, start_y, outline_color, bg_color):
        self.screen = screen
        self.square_size = square_size
        self.rows = rows
        self.columns = columns
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.start_x = start_x
        self.start_y = start_y
        self.outline_color = outline_color
        self.bg_color = bg_color

    def draw_grid(self):
        """
        Draws a grid of squares on the screen.
        """
        for row in range(self.rows):
            for col in range(self.columns):
                x = self.start_x + col * (self.square_size + self.x_spacing)
                y = self.start_y + row * (self.square_size + self.y_spacing)
                pygame.draw.rect(self.screen, self.bg_color, (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, self.outline_color, (x, y, self.square_size, self.square_size), 3)
        pygame.display.update()

    def draw_underlined_grid(self):
        """
        Draws a grid of squares with underlines on the screen.
        """
        for row in range(self.rows):
            for col in range(self.columns):
                x = self.start_x + col * (self.square_size + self.x_spacing)
                y = self.start_y + row * (self.square_size + self.y_spacing)
                pygame.draw.rect(self.screen, self.bg_color, (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, self.outline_color, (x, y, self.square_size, self.square_size), 3)
                underline_y = y + self.square_size + 5
                pygame.draw.line(self.screen, self.BLACK, (x, underline_y), (x + self.square_size, underline_y), 3)
        pygame.display.update()
