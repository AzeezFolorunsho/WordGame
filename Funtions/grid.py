import pygame

OUTLINE = "#d3d6da"

class Grid():
    # Calculate the number of squares to draw based on the word length and number of guesses.
    def __init__(self, screen,square_size, max_guesses, word_length, letter_x_spaces, letter_y_spaces, start_x, start_y) -> None:
        self.screen = screen
        self.square_size = square_size
        self.max_guesses = max_guesses
        self.word_length = word_length
        self.letter_x_spaces = letter_x_spaces
        self.letter_y_spaces = letter_y_spaces
        self.start_x = start_x
        self.start_y = start_y
    def draw_grid(self):
        # Draw the squares.
        for i in range(self.max_guesses):
            for j in range(self.word_length):
                x = self.start_x + j * (self.square_size + self.letter_x_spaces)
                y = self.start_y + i * (self.square_size + self.letter_y_spaces)
                pygame.draw.rect(self.screen, "white", (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, OUTLINE, (x, y, self.square_size, self.square_size), 3)
        pygame.display.update()