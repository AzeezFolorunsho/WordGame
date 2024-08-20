import pygame
import sys
from wordle_plus_game.src.components.buttons import TextButton, SliderButton, Dropdown
from wordle_plus_game.src.core.settings import Settings

class SettingsPage:
    def __init__(self, settings):
        """
        Initializes the settings page with the provided settings.
        """
        self.settings = settings
        self.setup_constants()
        self.setup_pygame()

        # Load avatars from the assets/avatars folder
        avatar_path = "wordle_plus_game/assets/avatars/"
        self.avatars = [f"Avatar {i}" for i in range(1, 13)]  # Display names for avatars

        # Dropdowns and buttons for settings
        self.username_field = TextButton("Username", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, 300, 100, 400, 45)
        
        self.avatar_dropdown = Dropdown(
            x=300,
            y=200,
            width=200,
            height=40,
            options=self.avatars,
            font=self.font,
            color_idle=self.BLACK,          # Updated to use color_idle
            color_hover=self.LIGHT_GREY,    # Updated to use color_hover
            color_active=self.LIGHT_GREY,   # Updated to use color_active
            text_color=self.WHITE
        )

        self.difficulty_dropdown = Dropdown(
            x=300,
            y=300,
            width=400,
            height=45,
            options=["Easy", "Normal", "Hard", "Ultra Hard", "Custom"],
            font=self.font,
            color_idle=self.BLACK,          # Updated to use color_idle
            color_hover=self.LIGHT_GREY,    # Updated to use color_hover
            color_active=self.LIGHT_GREY,   # Updated to use color_active
            text_color=self.WHITE
        )

        self.display_dropdown = Dropdown(
            x=300,
            y=400,
            width=400,
            height=45,
            options=["1280x720", "1366x768", "1600x900", "1920x1080"],
            font=self.font,
            color_idle=self.BLACK,          # Updated to use color_idle
            color_hover=self.LIGHT_GREY,    # Updated to use color_hover
            color_active=self.LIGHT_GREY,   # Updated to use color_active
            text_color=self.WHITE
        )

        self.return_button = TextButton("Return", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, self.screen_width - 140, self.screen_height / 2, 110, 45)

    def setup_constants(self):
        """
        Loads settings and constants.
        """
        self.screen_width = self.settings.get("General", "Screen Dimensions", {}).get("width", 1280)
        self.screen_height = self.settings.get("General", "Screen Dimensions", {}).get("height", 720)
        self.background_color = self.settings.get("General", "Background Color", "#FFFFFF")

        self.WHITE = "#FFFFFF"
        self.BLACK = "#000000"
        self.LIGHT_GREY = "#d3d6da"
        self.slider_color = (100, 100, 100)
        self.slider_hover_color = (150, 150, 150)

        self.font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 30)

    def setup_pygame(self):
        """
        Initializes Pygame, the screen, and the icon.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.icon = pygame.image.load("wordle_plus_game/assets/wordle+logo.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Wordle+ Settings")
        self.screen.fill(self.background_color)

    def settings_running(self, game_running):
        """
        Main loop for the settings page.
        """
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.avatar_dropdown.handle_event(event)
                self.difficulty_dropdown.handle_event(event)
                self.display_dropdown.handle_event(event)

            if self.return_button.draw(self.screen):
                game_running = False
                return

            self.avatar_dropdown.draw(self.screen)
            self.difficulty_dropdown.draw(self.screen)
            self.display_dropdown.draw(self.screen)
            self.return_button.draw(self.screen)

            pygame.display.flip()
