import pygame
from wordle_plus_game.src.components.buttons import TextButton

class OnScreenKeyboard:
    """
    Class representing an on-screen keyboard.

    Attributes:
        x (int): X-coordinate of the keyboard.
        y (int): Y-coordinate of the keyboard.
        x_spacing (int): Horizontal spacing between keys.
        y_spacing (int): Vertical spacing between keys.
        width (int): Width of each key.
        height (int): Height of each key.
        font (pygame.font.Font): Font for key labels.
        text_color (tuple): Text color for keys.
        bg_color (tuple): Background color for keys.
        hover_color (tuple): Hover color for keys.
    """

    LETTER_KEYS = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], 
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"], 
        ["ENT", "Z", "X", "C", "V", "B", "N", "M", "DEL"]
    ]

    def __init__(self, x, y, x_spacing, y_spacing, width, height, font, text_color, bg_color, hover_color):
        self.x = x
        self.y = y
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.width = width
        self.height = height
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.key_buttons = []

        self._initialize_keys()

    def _initialize_keys(self):
        """
        Initialize the keys on the keyboard and position them correctly.
        """
        current_x = self.x
        current_y = self.y

        for row_index, row in enumerate(self.LETTER_KEYS):
            for key in row:
                key_width = self.width
                if len(key) > 1:
                    key_width += self.width / 2 * (len(key) - 2)

                button = TextButton(key, self.font, self.text_color, self.bg_color, self.hover_color, current_x, current_y, key_width, self.height)
                self.key_buttons.append(button)

                current_x += key_width + self.x_spacing

            current_x = self.x
            current_y += self.height + self.y_spacing

            if row_index == 0:
                current_x += self.width / 2

    def update_key_color(self, letter, color):
        """
        Update the background color of a specific key.

        Args:
            letter (str): The key label to update.
            color (tuple): The new background color for the key.
        """
        for button in self.key_buttons:
            if button.text.upper() == letter.upper():
                button.bg_color_cache = color

    def reset_key_colors(self):
        """
        Reset the background color of all keys to the default.
        """
        for row in self.LETTER_KEYS:
            for letter in row:
                self.update_key_color(letter, self.bg_color)
