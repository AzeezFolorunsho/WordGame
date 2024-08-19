import pygame
import sys
from wordle_plus_game.src.components.buttons import TextButton, SliderButton
from wordle_plus_game.src.core.settings import Settings

class SettingsPage:
    def __init__(self, settings):
        """
        Initializes the settings page with the provided settings.
        """
        self.settings = settings
        self.setup_constants()
        self.setup_pygame()

        # Buttons and Sliders for settings
        self.return_button = TextButton(
            "Return", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY,
            self.screen_width - 140, self.screen_height / 2, 110, 45
        )

        self.width_slider = SliderButton(
            300, 200, 400, 30,
            800, 1920, self.screen_width,
            self.slider_color, self.slider_hover_color
        )
        
        self.height_slider = SliderButton(
            300, 300, 400, 30,
            600, 1080, self.screen_height,
            self.slider_color, self.slider_hover_color
        )
        
        self.bg_color_button = TextButton(
            "Toggle Background", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY,
            300, 400, 200, 45
        )

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

    def toggle_background_color(self):
        """
        Toggles between light and dark mode.
        """
        if self.background_color == self.settings.preset_colors["light_mode"]:
            self.background_color = self.settings.preset_colors["dark_mode"]
        else:
            self.background_color = self.settings.preset_colors["light_mode"]
        self.settings.set("General.Background Color", self.background_color)
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

            if self.return_button.draw(self.screen):
                game_running = False
                return

            self.screen_width = self.width_slider.draw(self.screen)
            self.screen_height = self.height_slider.draw(self.screen)
            self.settings.set("General", "Screen Dimensions.width", self.screen_width)
            self.settings.set("General", "Screen Dimensions.height", self.screen_height)

            if self.bg_color_button.draw(self.screen):
                self.toggle_background_color()

            pygame.display.flip()

        pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(self.background_color)
