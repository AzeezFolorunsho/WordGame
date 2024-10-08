import pygame
import sys
from wordle_plus_game.src.components.buttons import TextButton, Dropdown
from wordle_plus_game.src.utils.avatar import Avatar

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

        saved_avatar = f"Avatar {(self.settings.get('User Profiles', 'Current Avatar', 'wordle_plus_game/assets/avatars/avatar1.png'))[-5]}"
        saved_difficulty = self.settings.get("Game Settings", "Current Difficulty Level", "Normal")
        saved_resolution = f'{self.settings.get("General", "Screen Dimensions", {}).get("width")}x{self.settings.get("General", "Screen Dimensions", {}).get("height")}'

        self.avatar = Avatar(x=150, y=100, scale=0.8)
        
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
            text_color=self.WHITE,
            bg_color=self.background_color
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
            text_color=self.WHITE,
            bg_color=self.background_color
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
            text_color=self.WHITE,
            bg_color=self.background_color
        )
        self.display_dropdown.selected_option = saved_resolution

        self.return_button = TextButton("Return", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, self.screen_width - (self.screen_width / 6), 100, 110, 30)

        self.save_button = TextButton("Save", self.font, self.WHITE, self.BLACK, self.LIGHT_GREY, 300, 100, 110, 30)

        self.color_mapping = {
            "#FFFFFF": "White",
            "#000000": "Black",
            "#FF0000": "Red",
            "#00FF00": "Green",
            "#0000FF": "Blue",
            "#A4E1EA": "Light Blue"
        }

        self.background_colors = list(self.color_mapping.keys())

        saved_bg_color = self.settings.get("General", "Background Color", "#FFFFFF")

        self.bg_color_dropdown = Dropdown(
            x=300,
            y=500,  # Position it below other elements
            width=400,
            height=45,
            options=[f"{self.color_mapping[color]} ({color})" for color in self.background_colors],
            font=self.font,
            color_idle=self.BLACK,
            color_hover=self.LIGHT_GREY,
            color_active=self.LIGHT_GREY,
            text_color=self.WHITE,
            bg_color=self.background_color
        )
        self.bg_color_dropdown.selected_option = f"{self.color_mapping[saved_bg_color]} ({saved_bg_color})"
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
        self.settings.set("User Profiles", "Current Avatar", f"wordle_plus_game/assets/avatars/avatar{selected_avatar[-1]}.png")

        selected_difficulty = self.difficulty_dropdown.selected_option
        self.settings.set("Game Settings", "Current Difficulty Level", selected_difficulty)

        selected_resolution = self.display_dropdown.selected_option.split('x')

        self.settings.set("General", "Screen Dimensions", {
        "width": int(selected_resolution[0]),
        "height": int(selected_resolution[1])
        })

        selected_bg_color = self.bg_color_dropdown.selected_option.split()[-1].strip("()")
        self.settings.set("General", "Background Color", selected_bg_color)

    def settings_running(self, game_running):
        """
        Main loop for the settings page.
        """
        clock = pygame.time.Clock()
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.avatar_dropdown.handle_event(event)
                self.difficulty_dropdown.handle_event(event)
                self.display_dropdown.handle_event(event)
                self.bg_color_dropdown.handle_event(event)

            if self.return_button.draw(self.screen):
                game_running = False
                return

            if self.save_button.draw(self.screen):
                self.save_settings()
                self.__init__(self.settings)

            self.avatar.draw(self.screen)
            self.avatar_dropdown.draw(self.screen)
            self.difficulty_dropdown.draw(self.screen)
            self.display_dropdown.draw(self.screen)
            self.bg_color_dropdown.draw(self.screen)

            clock.tick(60)

            pygame.display.flip()
