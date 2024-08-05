import pygame

class Textbox_grid():
    # Calculate the number of squares to draw based on the word length and number of guesses.
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
        # Draw the squares.
        for i in range(self.rows):
            for j in range(self.columns):
                x = self.start_x + j * (self.square_size + self.x_spacing)
                y = self.start_y + i * (self.square_size + self.y_spacing)
                pygame.draw.rect(self.screen, self.bg_color, (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, self.outline_color, (x, y, self.square_size, self.square_size), 3)
        pygame.display.update()