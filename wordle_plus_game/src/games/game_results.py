import pygame
from wordle_plus_game.src.components.text import Text

class GameResults:
    """
    A class for displaying game results including messages, scores, and word reveals.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the results box.
        y (int): The y-coordinate of the top-left corner of the results box.
        font (pygame.font.Font): The font used for rendering text.
        text_color (tuple): The color of the text.
        bg_color (tuple): The background color of the results box.
        max_box_width (int): Maximum width of the results box.
        finish_message (str): Message to display upon finishing the game.
        score (int): Score achieved in the game.
        replay_message (str): Message prompting replay.
        word_reveal (list): List of words to reveal as part of the results.
    """

    def __init__(self, x, y, font, text_color=(0, 0, 0), bg_color=(255, 255, 255), max_box_width=500, finish_message="Game Over!", score=0, replay_message="Press ENTER to Play Again!", word_reveal=None):
        if word_reveal is None:
            word_reveal = []

        self.x = x
        self.y = y
        self.max_box_width = max_box_width
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color

        # Messages
        self.finish_message = finish_message
        self.word_reveal = word_reveal
        self.word_list = ", ".join(self.word_reveal)
        self.score = score
        self.replay_message = replay_message

        # Text objects
        self.finish_message_text = Text(self.finish_message, self.font, self.x, self.y, max_width=self.max_box_width, text_color=self.text_color)
        self.word_reveal_text = Text(f"The Word(s) were: {self.word_list}", self.font, self.x, self.finish_message_text.y + self.finish_message_text.height, max_width=self.font.size("The Word(s) were: ________ ")[0], text_color=self.text_color)
        self.score_text = Text(f"The Score was: {self.score}", self.font, self.x, self.word_reveal_text.y + self.word_reveal_text.height, max_width=self.max_box_width, text_color=self.text_color)
        self.replay_message_text = Text(self.replay_message, self.font, self.x, self.score_text.y + self.score_text.height, max_width=self.max_box_width, text_color=self.text_color)

        # Background size determination
        self.longest_line = max(self.finish_message_text.width, self.word_reveal_text.width, self.score_text.width, self.replay_message_text.width)
        self.message_height = self.finish_message_text.height + self.word_reveal_text.height + self.score_text.height + self.replay_message_text.height

        # Results box
        self.background_rect = pygame.Rect(self.x, self.y, self.longest_line, self.message_height)

    def set_finish_message(self, message):
        """
        Sets a new finish message and updates the results display.

        Args:
            message (str): The new finish message to set.
        """
        self.finish_message = message
        self.draw_results()

    def draw_results(self, screen):
        """
        Draws the results box with all associated text on the screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        pygame.draw.rect(screen, self.bg_color, self.background_rect)
        self.finish_message_text.draw(screen)
        self.word_reveal_text.draw(screen)
        self.score_text.draw(screen)
        self.replay_message_text.draw(screen)

        pygame.display.update()
