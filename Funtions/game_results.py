import pygame
from Funtions.text import Text

class Game_Results:
    def __init__ (self, x, y, font, text_color, bg_color, finish_message, score, replay_message, *word_reveal):
        self.x = x
        self.y = y
        self.max_box_width = 500
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        
        # messages
        self.finish_message = finish_message
        self.word_reveal = word_reveal
        self.word_list = ", ".join(word for word in self.word_reveal)
        self.score = score
        self.replay_message = replay_message
    
        # text objects
        self.finish_message_text = Text(self.finish_message, self.font, self.text_color, self.x, self.y, self.max_box_width)
        self.word_reveal_text = Text("The Word(s) were: " + self.word_list, self.font, self.text_color, self.x, (self.finish_message_text.y + self.finish_message_text.height), self.font.size("The Word(s) were: ________ ")[0])
        self.score_text = Text("The Score was: " + self.score, self.font, self.text_color, self.x, (self.word_reveal_text.y + self.word_reveal_text.height), self.max_box_width)
        self.replay_message_text = Text(self.replay_message, self.font, self.text_color, self.x, (self.score_text.y + self.score_text.height), self.max_box_width)
        
        # baground size determination
        self.longest_line = max(self.finish_message_text.width, self.word_reveal_text.width, self.score_text.width, self.replay_message_text.width)
        self.message_height = self.finish_message_text.height + self.word_reveal_text.height + self.score_text.height + self.replay_message_text.height

        # messages box
        self.background_rect = pygame.Rect(self.x, self.y, self.longest_line, self.message_height)

    def set_finish_message(self, message):
        self.finish_message = message
        self.draw_results()

    def draw_results(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.background_rect)
        self.finish_message_text.draw_line(screen)
        self.word_reveal_text.draw_wrapped(screen)
        self.score_text.draw_line(screen)
        self.replay_message_text.draw_line(screen)

        pygame.display.update()