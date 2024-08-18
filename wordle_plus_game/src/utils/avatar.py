import pygame

class Avatar:
    def __init__(self, x, y, scale, settings):
        self.x = x
        self.y = y
        self.scale = scale
        self.settings = settings
        self.avatar_file= self.settings.get("User Profiles", "Current Avatar", "wordle_plus_game/assets/avatars/avatar1.png")
        self.avatar_img= pygame.image.load(self.avatar_file)
        width = self.avatar_img.get_width()
        height = self.avatar_img.get_height()
        self.avatar_img = pygame.transform.scale(self.avatar_img, (int(width * scale), int(height * scale)))
        self.avatar_rect = self.avatar_img.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.avatar_img, self.avatar_rect)