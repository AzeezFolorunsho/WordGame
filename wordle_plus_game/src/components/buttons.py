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
    
class SliderButton:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = False
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

        # you didint set these but used them, it caused errors, I dont know if these are correct values, but it works, please fix
        self.handle_pos = self.rect.x + self.value / (self.max_value - self.min_value) * self.rect.width
        self.dragging = False


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the slider handle
        handle_rect = pygame.Rect(self.handle_pos - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, self.hover_color if self.dragging else self.color, handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_pos = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                self.value = self.min_val + (self.handle_pos - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.value
    
class Dropdown:
    def __init__(self, x, y, width, height, options, font=None, color_idle=(200, 200, 200), color_hover=(100, 100, 100), color_active=(50, 50, 50), text_color=(0, 0, 0)):
        """
        Initializes the dropdown menu.

        Args:
            options (list): A list of strings representing the options in the dropdown.
            x (int): The x-coordinate of the dropdown.
            y (int): The y-coordinate of the dropdown.
            width (int): The width of the dropdown.
            height (int): The height of the dropdown.
            font (pygame.font.Font, optional): The font used for the dropdown text.
            color_idle (tuple): RGB color for the idle state.
            color_hover (tuple): RGB color for the hover state.
            color_active (tuple): RGB color for the active (expanded) state.
            text_color (tuple): RGB color for the text.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.font = font if font else pygame.font.Font(None, 30)
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.color_active = color_active
        self.text_color = text_color
        self.selected_option = options[0] if options else None
        self.is_open = False
        self.rect = pygame.Rect(x, y, width, height)

    def handle_event(self, event):
        """
        Handles events related to the dropdown menu.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
            elif self.is_open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.height, self.width, self.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = option
                        self.is_open = False

    def draw(self, screen):
        """
        Draws the dropdown menu on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the dropdown on.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.color_hover, self.rect)
        else:
            pygame.draw.rect(screen, self.color_idle, self.rect)

        # Draw the selected option
        selected_text = self.font.render(self.selected_option, True, self.text_color)
        screen.blit(selected_text, selected_text.get_rect(center=self.rect.center))

        if self.is_open:
            # Draw dropdown options
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.height, self.width, self.height)
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, self.color_hover, option_rect)
                else:
                    pygame.draw.rect(screen, self.color_active, option_rect)
                
                option_text = self.font.render(option, True, self.text_color)
                screen.blit(option_text, option_text.get_rect(center=option_rect.center))
        
        pygame.draw.rect(screen, self.text_color, self.rect, 2)

    def get_value(self):
        """
        Returns the currently selected option.

        Returns:
            str: The selected option.
        """
        return self.selected_option