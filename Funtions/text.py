import pygame

class Text:
    def __init__(self, text, font, color, x, y, max_width):
        self.font = font
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.max_width = max_width

        # text rendering
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.topleft = (self.x, self.y)
        
        # text wrapping
        self.wraped_text = self.wrap_text()
        self.line_number = len(self.wraped_text)
        
        self.longest_line = max(self.wraped_text, key=lambda line: line.get_width())

        # text size
        self.width = self.longest_line.get_width()
        self.height = self.rendered_text.get_height() * self.line_number

    def draw_line(self, surface):
        surface.blit(self.rendered_text, self.text_rect)

    def wrap_text(self):
        words = self.text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return [self.font.render(line, True, self.color) for line in lines]

    def draw_wrapped(self, surface):
        y_offset = 0
        for line in self.wraped_text:
            surface.blit(line, (self.x, self.y + y_offset))
            y_offset += self.font.get_linesize()
