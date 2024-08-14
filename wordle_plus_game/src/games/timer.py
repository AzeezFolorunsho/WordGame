import pygame
from wordle_plus_game.src.components.text import Text

class Timer:
    """
    A class to manage a countdown timer in a Pygame application.

    Attributes:
        screen (pygame.Surface): The Pygame surface to draw the timer on.
        x (int): The x-coordinate of the timer display.
        y (int): The y-coordinate of the timer display.
        background_color (tuple): The background color for the timer display.
        font (pygame.font.Font): The font used for rendering the timer text.
    """

    def __init__(self, screen, x, y, background_color, font):
        self.screen = screen
        self.x = x
        self.y = y
        self.background_color = background_color
        self.font = font

        self.start_time = 0
        self.is_active = False
        self.elapsed_time = 0

    def start(self):
        """
        Activates the timer, setting the start time.
        """
        self.is_active = True
        self.elapsed_time = 0
        self.start_time = pygame.time.get_ticks()

    def draw(self):
        """
        Draws the timer on the screen.
        """
        if self.is_active:
            current_time = pygame.time.get_ticks()
            self.elapsed_time = (current_time - self.start_time) // 1000
            time_msg = Text(f"Timer: {self.elapsed_time}", self.font, self.x, self.y, bg_color=self.background_color)
            time_msg.draw(self.screen)

    def stop(self):
        """
        Stops the timer and returns the elapsed time.

        Returns:
            int: The elapsed time in seconds.
        """
        self.is_active = False
        self.start_time = 0
        return self.elapsed_time
