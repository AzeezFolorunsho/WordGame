import pygame
import sys
from wordle_plus_game.src.core.settings import Settings
from wordle_plus_game.src.components.buttons import TextButton
from wordle_plus_game.src.games.WordleClassic import WordleClassic
from wordle_plus_game.src.games.WordleHangman import WordleHangman

class Menu:
    """
    Class for managing the main menu and game selection.

    Attributes:
        settings (Settings): Game settings.
        screen (pygame.Surface): The Pygame screen surface for rendering the menu.
        buttons (list): List of TextButton objects representing menu options.
    """

    def __init__(self, settings):
        self.settings = settings
        self.screen_width = self.settings.get("General", "Screen Dimensions", {}).get("width", 1280)
        self.screen_height = self.settings.get("General", "Screen Dimensions", {}).get("height", 720)
        self.bg_color = self.settings.get("General", "Background Color", "#FFFFFF")

        self.init_pygame()
        self.init_fonts()
        self.init_buttons()

    def init_pygame(self):
        """
        Initializes Pygame and sets up the screen.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.icon = pygame.image.load("wordle_plus_game/assets/wordle+logo.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Wordle+ Menu")
        self.screen.fill(self.bg_color)

    def init_fonts(self):
        """
        Initializes fonts for the menu.
        """
        self.button_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 35)

    def init_buttons(self):
        """
        Initializes the menu buttons.
        """
        self.buttons = [
            TextButton("Play Wordle Classic", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 250, 400, 50),
            TextButton("Play Wordle Hangman", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 350, 400, 50),
            TextButton("Quit", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 450, 400, 50)
        ]

    def display_menu(self):
        """
        Displays the main menu and handles button interactions.
        """
        running = True
        while running:
            for button in self.buttons:
                action = button.draw(self.screen)
                if action:
                    if action == "Play Wordle Classic":
                        self.play_wordle_classic()
                    elif action == "Play Wordle Hangman":
                        self.play_wordle_hangman()
                    elif action == "Quit":
                        running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def play_wordle_classic(self):
        """
        Launches the Wordle Classic game.
        """
        game = WordleClassic(self.settings)
        game.game_loop(True)
        self.screen.fill(self.bg_color)

    def play_wordle_hangman(self):
        """
        Launches the Wordle Hangman game.
        """
        game = WordleHangman(self.settings)
        game.game_loop(True)
        self.screen.fill(self.bg_color)

def main():
    """
    Main function to run the Wordle Plus game.
    """
    # Initialize settings
    settings = Settings()

    # Create the main menu
    menu = Menu(settings)

    # Display the menu
    menu.display_menu()

if __name__ == "__main__":
    main()
