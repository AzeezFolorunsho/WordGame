import pygame
from Funtions.text import Text

class Timer:
    def __init__(self, screen, x, y, background_color):
        self.screen = screen
        self.x = x
        self.y = y
        self.background_color = background_color

        self.start_time = 0
        self.active = False
        self.time_passed = 0
        self.TIMER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)
        
    def activate_timer(self):
        self.active = True
        self.time_passed = 0
        self.start_time = pygame.time.get_ticks()

    def draw(self):
        if self.active == True:
            current_time = pygame.time.get_ticks()
            self.time_passed = (current_time - self.start_time) // 1000

            # draws timer on screen
            time_msg = Text("Timer: " + str(self.time_passed), self.TIMER_FONT, "#000000", self.x, self.y, 0)
            pygame.draw.rect(self.screen, self.background_color, (time_msg.text_rect)) # draws white background
            time_msg.draw_line(self.screen)
            
    def stop_timer(self):
        self.active = False
        self.start_time = 0
        return self.time_passed