import pygame
import sys
from wordle_plus_game.src.core.settings import Settings
from wordle_plus_game.src.components.buttons import TextButton
from wordle_plus_game.src.games.WordleClassic import WordleClassic
from wordle_plus_game.src.games.WordleHangman import WordleHangman
from wordle_plus_game.src.games.SettingsPage import SettingsPage
from wordle_plus_game.src.components.text import Text
from wordle_plus_game.src.utils.avatar import Avatar
from wordle_plus_game.src.games.ScoreBoard import ScoreBoard

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

        # username
        self.username = self.settings.get("User Profiles", "Username", "Player")
        self.username_size = self.title_font.size(self.username)[0]
        self.username_x = (self.screen_width / 2) - (self.username_size / 2)
        self.username_text = Text(self.username, self.title_font, self.username_x, 150)
        self.username_x_spacing = 85
        
        # welcome image
        self.welcome_image = pygame.image.load("wordle_plus_game/assets/welcome.png")
        self.welcome_width = self.welcome_image.get_width()
        self.welcome_height = self.welcome_image.get_height()
        self.welcome_scaled = pygame.transform.scale(self.welcome_image, (self.welcome_width * 0.95, self.welcome_height * 0.95))
        self.scaled_width = self.welcome_scaled.get_width()

        self.avatar = Avatar(self.username_x - self.username_x_spacing, 150, 0.8)

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
            TextButton("Play Wordle Hangman", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 350, 400, 50),
            TextButton("Settings", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width - (self.screen_width / 6), 50, 150, 50),
            TextButton("Classic Scoreboard", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 450, 400, 50),
            TextButton("Hangman Scoreboard", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 550, 400, 50),
            TextButton("Quit", self.button_font, (255, 255, 255), (0, 0, 0), (128, 128, 128), self.screen_width / 2 - 200, 650, 400, 50)
        ]

    def display_menu(self):
        """
        Displays the main menu and handles button interactions.
        """

        running = True
        while running:

            self.screen.blit(self.menu_bg, [0, 0])
            self.screen.blit(self.welcome_scaled, [((self.screen_width / 2) - (self.scaled_width / 2)), 20])
            self.username_text.draw(self.screen)

            self.avatar.draw(self.screen)

            for button in self.buttons:
                action = button.draw(self.screen)
                if action:
                    if action == "Play Wordle Classic":
                        self.play_wordle_classic()
                    elif action == "Play Wordle Hangman":
                        self.play_wordle_hangman()
                    elif action == "Settings":
                        self.start_settings()
                    elif action == "Classic Scoreboard":
                        self.view_scoreboard("Classic")
                    elif action == "Hangman Scoreboard":
                        self.view_scoreboard("Hangman")
                    elif action == "Quit":
                        running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def view_scoreboard(self, game_mode):
        """
        Displays the scoreboard for the selected game mode.
        """
        scoreboard = ScoreBoard(self.settings, game_mode)
        scoreboard.run(True)
        self.screen.fill(self.bg_color)

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

    def start_settings(self):
        """
        Launches Settings page.
        """
        settings_page = SettingsPage(self.settings)
        settings_page.settings_running(True)
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
