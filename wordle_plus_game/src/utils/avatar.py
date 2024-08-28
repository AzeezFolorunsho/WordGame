import pygame
from wordle_plus_game.src.core.settings import Settings

class Avatar:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale

    def draw(self, screen):
        self._create_img()
        screen.blit(self.avatar_img, self.avatar_rect)
        # draw a circle around the avatar
        pygame.draw.circle(
            screen,
            "#FFFFFF", 
            (self.x + self.width / 2.5, self.y + self.height / 2.5), 
            self.avatar_img.get_width() / 2 + 5, 
            5
            )
    
    def _create_img(self):
        self.settings = Settings()

        self.avatar_file = self.settings.get("User Profiles", "Current Avatar", "wordle_plus_game/assets/avatars/avatar1.png")
        self.avatar_img = pygame.image.load(self.avatar_file)

        self.width = self.avatar_img.get_width()
        self.height = self.avatar_img.get_height()

        self.avatar_img = pygame.transform.scale(self.avatar_img, (int(self.width * self.scale), int(self.height * self.scale)))
        self.avatar_rect = self.avatar_img.get_rect(topleft=(self.x, self.y))