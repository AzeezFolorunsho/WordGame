import pygame
import sys
from wordle_plus_game.src.core.settings import Settings
from wordle_plus_game.src.components.buttons import TextButton
from wordle_plus_game.src.games.WordleClassic import WordleClassic
from wordle_plus_game.src.games.WordleHangman import WordleHangman
from wordle_plus_game.src.components.text import Text
from wordle_plus_game.src.utils.avatar import Avatar

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
        
        # Wordle-inspired background images
        self.menu_image = pygame.image.load("wordle_plus_game/assets/background_images/menu_background.png")
        self.menu_bg = pygame.transform.scale(self.menu_image, (self.screen_width, self.screen_height))
        
        self.init_pygame()
        self.init_fonts()
        self.init_buttons()

        self.title_size = self.title_font.size("Welcome to Wordle+!")[0]
        self.username = self.settings.get("User Profiles", "Username", "Player")
        self.username_size = self.title_font.size(self.username)[0]
        self.username_x = (self.screen_width / 2) - (self.username_size / 2)
        self.username_text = Text(self.username, self.title_font, self.username_x, 150)
        self.username_x_spacing = 85
        
        # welcome image
        self.welcome_image = pygame.image.load("wordle_plus_game/assets/welcome.png")
        self.welcome_width = self.welcome_image.get_width()
        self.welcome_height = self.welcome_image.get_height()
        self.welcome_scaled = pygame.transform.scale(self.screen, (100, 100))

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
        self.title_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 50)

    def init_buttons(self):
        """
        Initializes the menu buttons.
        """
        self.buttons = [
            TextButton("Play Wordle Classic", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 250, 400, 50),
            TextButton("Play Wordle Hangman", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 325, 400, 50),
            TextButton("Quit", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 400, 400, 50)
        ]

    def display_menu(self):
        """
        Displays the main menu and handles button interactions.
        """
        avatar = Avatar(x = self.username_x - self.username_x_spacing, y = 150, scale=0.8, settings=self.settings)
        
        running = True
        while running:

            self.screen.blit(self.menu_bg, [0, 0])
            self.screen.blit(self.welcome_image, [((self.screen_width / 2) - (self.welcome_width / 2)), 20])
            self.username_text.draw(self.screen)

            avatar.draw(self.screen)

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
