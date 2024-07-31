import pygame

# Button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def set_xand_y(self, x, y):
        self.rect.topleft = (x, y)
        
    def draw(self, screen):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        
        # Mouseover & clicking
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        # Draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action