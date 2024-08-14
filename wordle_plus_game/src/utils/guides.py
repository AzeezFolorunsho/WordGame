import pygame

class Guide:
    """
    Class for drawing guide lines on the screen for alignment and layout purposes.

    Attributes:
        screen (pygame.Surface): The Pygame surface to draw the guides on.
    """

    def __init__(self, screen):
        self.screen = screen

    def draw_cross_guides(self, color):
        """
        Draws cross guides dividing the screen into four quadrants.

        Args:
            color (tuple): The color of the guide lines.
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Horizontal line
        pygame.draw.line(self.screen, color, (0, screen_height / 2), (screen_width, screen_height / 2), 2)

        # Vertical line
        pygame.draw.line(self.screen, color, (screen_width / 2, 0), (screen_width / 2, screen_height), 2)

        pygame.display.update()

    def draw_third_guides(self, color):
        """
        Draws vertical guides dividing the screen into thirds.

        Args:
            color (tuple): The color of the guide lines.
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # First third
        pygame.draw.line(self.screen, color, (screen_width / 3, 0), (screen_width / 3, screen_height), 2)

        # Second third
        pygame.draw.line(self.screen, color, (screen_width / 3 * 2, 0), (screen_width / 3 * 2, screen_height), 2)

        pygame.display.update()
