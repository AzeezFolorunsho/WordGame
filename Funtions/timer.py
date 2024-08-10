import pygame
from Funtions.text import Text

class Timer:
    def __init__(self, screen, x, y, background_color):
        self.screen = screen
        self.x = x
        self.y = y
        self.background_color = background_color
        self.time = 0
        self.round_running = True
        self.TIMER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 30)
        
    def draw(self):
        if self.round_running == True:
            self.time += 1
            time_msg = Text("Timer: " + str(self.time), self.TIMER_FONT, "#000000", self.x, self.y, 100)
            pygame.draw.rect(self.screen, self.background_color, (time_msg.text_rect))
            time_msg.draw_line(self.screen)
            
    def pause_time(self):
        self.round_running = False
        return self.time
    
    def reset_timer(self):
        self.time = 0
        self.round_running = True
        