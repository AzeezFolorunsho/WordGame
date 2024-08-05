import pygame

class Guide:
    def __init__ (self, screen):
        self.screen = screen
    def draw_guides_cross(self, color):
        pygame.draw.rect(self.screen, color, ((0, self.screen.get_height()/2), (self.screen.get_width(), 2)))
        pygame.draw.rect(self.screen, color, ((self.screen.get_width()/2, 0), (2, self.screen.get_height())))
        pygame.display.update()

    def draw_guides_thirds(self, color):
        pygame.draw.rect(self.screen, color, ((self.screen.get_width()/3, 0), (2, self.screen.get_height())))
        pygame.draw.rect(self.screen, color, ((self.screen.get_width()/3 * 2, 0), (2, self.screen.get_height())))
        pygame.display.update()