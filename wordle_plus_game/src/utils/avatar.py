import pygame
from wordle_plus_game.src.core.settings import Settings

class Avatar:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.settings = Settings()
        

    def draw(self, screen):
        self._create_img()
        screen.blit(self.avatar_img, self.avatar_rect)
    
    def _create_img(self):
        self.avatar_file = self.settings.get("User Profiles", "Current Avatar", "wordle_plus_game/assets/avatars/avatar1.png")
        self.avatar_file= self.settings.get("User Profiles", "Current Avatar", "wordle_plus_game/assets/avatars/avatar1.png")
        self.avatar_img= pygame.image.load(self.avatar_file)
        width = self.avatar_img.get_width()
        height = self.avatar_img.get_height()
        self.avatar_img = pygame.transform.scale(self.avatar_img, (int(width * self.scale), int(height * self.scale)))
        self.avatar_rect = self.avatar_img.get_rect(topleft=(self.x, self.y))