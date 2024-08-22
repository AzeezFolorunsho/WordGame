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

        avatar_path = "wordle_plus_game/assets/avatars/"
        self.avatars = [f"Avatar {i}" for i in range(1, 13)] 

        saved_avatar = self.settings.get("User Profile", "Avatar", self.avatars[0])
        saved_difficulty = self.settings.get("Game Settings", "Difficulty", "Normal")
        saved_resolution = f'{self.settings.get("Display", "Width", 1280)}x{self.settings.get("Display", "Height", 720)}' 

        self.username_field = TextButton("Username", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, 300, 100, 400, 45)
        
        self.avatar_dropdown = Dropdown(
            x=300,
            y=200,
            width=200,
            height=40,
            options=self.avatars,
            font=self.font,
            color_idle=self.BLACK,          
            color_hover=self.LIGHT_GREY,    
            color_active=self.LIGHT_GREY,   
            text_color=self.WHITE
        )
        self.avatar_dropdown.selected_option = saved_avatar

        self.difficulty_dropdown = Dropdown(
            x=300,
            y=300,
            width=400,
            height=45,
            options=["Easy", "Normal", "Hard", "Ultra Hard", "Custom"],
            font=self.font,
            color_idle=self.BLACK,          
            color_hover=self.LIGHT_GREY,    
            color_active=self.LIGHT_GREY,   
            text_color=self.WHITE
        )
        self.difficulty_dropdown.selected_option = saved_difficulty

        self.display_dropdown = Dropdown(
            x=300,
            y=400,
            width=400,
            height=45,
            options=["1280x720", "1366x768", "1600x900", "1920x1080"],
            font=self.font,
            color_idle=self.BLACK,          
            color_hover=self.LIGHT_GREY,    
            color_active=self.LIGHT_GREY,   
            text_color=self.WHITE
        )
        self.display_dropdown.selected_option = saved_resolution

        self.return_button = TextButton("Return", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, self.screen_width - (self.screen_width / 6), 10, 110, 30)

        self.save_button = TextButton("Save", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, 300, 100, 110, 30)

    def setup_constants(self):
        """
        Loads settings and constants.
        """
        self.screen_width = self.settings.get("General", "Screen Dimensions", 1280).get("width")
        self.screen_height = self.settings.get("General", "Screen Dimensions", 720).get("height")
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

    def save_settings(self):
        """
        Save the current settings from the dropdowns and fields.
        """
        selected_avatar = self.avatar_dropdown.selected_option
        self.settings.set("User Profile", "Avatar", selected_avatar)

        selected_difficulty = self.difficulty_dropdown.selected_option
        self.settings.set("Game Settings", "Difficulty", selected_difficulty)

        selected_resolution = self.display_dropdown.selected_option.split('x')
        self.settings.set("Display", "Width", int(selected_resolution[0]))
        self.settings.set("Display", "Height", int(selected_resolution[1]))

        self.settings.set("General", "Screen Dimensions", {
        "width": int(selected_resolution[0]),
        "height": int(selected_resolution[1])
        })

        self.apply_new_resolution()
        self.notify_main_menu()

    def notify_main_menu(self):
        """
        Notify the main menu or other screens about the settings change.
        """
        if hasattr(self, 'main_menu'):
            self.main_menu.update_settings()

    def apply_new_resolution(self):
        new_width = self.settings.get("Display", "Width", 1280)
        new_height = self.settings.get("Display", "Height", 720)

        self.screen = pygame.display.set_mode((new_width, new_height))
        self.screen.fill(self.background_color)
        pygame.display.flip()

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

            if self.save_button.draw(self.screen):
                self.save_settings()
                self.apply_new_resolution()

            self.avatar_dropdown.draw(self.screen)
            self.difficulty_dropdown.draw(self.screen)
            self.display_dropdown.draw(self.screen)
            self.return_button.draw(self.screen)
            self.save_button.draw(self.screen)

            pygame.display.flip()
