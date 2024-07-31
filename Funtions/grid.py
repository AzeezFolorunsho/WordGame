import pygame

OUTLINE = "#d3d6da"

class Text_box_grid():
    # Calculate the number of squares to draw based on the word length and number of guesses.
    def __init__(self,square_size, rows, columns, x_spacing, y_spacing, start_x, start_y):
        self.square_size = square_size
        self.rows = rows
        self.columns = columns
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.start_x = start_x
        self.start_y = start_y
    def draw_grid(self, screen):
        self.screen = screen
        # Draw the squares.
        for i in range(self.rows):
            for j in range(self.columns):
                x = self.start_x + j * (self.square_size + self.x_spacing)
                y = self.start_y + i * (self.square_size + self.y_spacing)
                pygame.draw.rect(self.screen, "white", (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, OUTLINE, (x, y, self.square_size, self.square_size), 3)
        pygame.display.update()