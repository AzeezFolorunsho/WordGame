import pygame

# Button class
class img_Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def set_x_and_y(self, x, y):
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
    
class Text_Button:
    def __init__(self, text, font, text_color, bg_color, x, y, widith, height):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.width = widith
        self.height = height
        self.text_position = (self.x + (self.width / 2), self.y + (self.height / 2))
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)
        self.clicked = False

    def set_x_and_y(self, x_pos, y_pos):
        self.x = x_pos 
        self.y = y_pos    

    def set_width_and_height(self, widith_size, height_size):
        self.width = widith_size
        self.height = height_size
    
    def get_text(self):
        return self.text
    
    def draw(self, screen):
        # Draws the button background and text
        pygame.draw.rect(screen, self.bg_color, self.text_rect)
        screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        
        # Mouseover & clicking
        if self.text_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return self.text if action == True else False