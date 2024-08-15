import pygame

class ImageButton:
    """
    A class for managing image-based buttons in a Pygame application.

    Attributes:
        image (pygame.Surface): The image displayed for the button.
        rect (pygame.Rect): The rectangle defining the button's position and size.
        clicked (bool): Whether the button is currently clicked.
    """

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def set_position(self, x, y):
        """
        Sets a new position for the button.

        Args:
            x (int): New x-coordinate for the button.
            y (int): New y-coordinate for the button.
        """
        self.rect.topleft = (x, y)

    def draw(self, screen):
        """
        Draws the button on the screen and checks for clicks.

        Args:
            screen (pygame.Surface): The Pygame surface to draw the button on.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class TextButton:
    """
    A class for managing text-based buttons in a Pygame application.

    Attributes:
        text (str): The text displayed on the button.
        font (pygame.font.Font): The font used for the button text.
        text_color (tuple): The color of the button text.
        bg_color (tuple): The background color of the button.
        hover_color (tuple): The color of the button when hovered.
        x (int): The x-coordinate of the top-left corner of the button.
        y (int): The y-coordinate of the top-left corner of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        text_position (tuple): The position of the text within the button.
        text_surface (pygame.Surface): The surface containing the rendered text.
        text_rect (pygame.Rect): The rectangle defining the text's position and size.
        bg_rect (pygame.Rect): The rectangle defining the button's position and size.
        clicked (bool): Whether the button is currently clicked.
    """

    def __init__(self, text, font, text_color, bg_color, hover_color, x, y, width, height):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.bg_color_cache = bg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text_position = (self.x + self.width / 2, self.y + self.height / 2)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)
        self.bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.clicked = False

    def set_position(self, x, y):
        """
        Sets a new position for the button.

        Args:
            x (int): New x-coordinate for the button.
            y (int): New y-coordinate for the button.
        """
        self.x = x
        self.y = y

    def set_size(self, width, height):
        """
        Sets a new size for the button.

        Args:
            width (int): New width for the button.
            height (int): New height for the button.
        """
        self.width = width
        self.height = height

    def draw(self, screen):
        """
        Draws the button on the screen and checks for clicks.

        Args:
            screen (pygame.Surface): The Pygame surface to draw the button on.

        Returns:
            Optional[str]: The text of the button if clicked, None otherwise.
        """
        pygame.draw.rect(screen, self.bg_color, self.bg_rect)
        screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

        action = False
        pos = pygame.mouse.get_pos()

        if self.bg_rect.collidepoint(pos):
            self.bg_color = self.hover_color
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.bg_color = self.bg_color_cache

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return self.text if action else None
