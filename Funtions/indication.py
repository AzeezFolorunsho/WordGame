import pygame

class Indication:
    def __init__(self, on_screen_keyboard, guesses):
        self.on_screen_keyboard = on_screen_keyboard
        self.guesses = guesses

    def update_bg_color(self, letter, color):
        # for keys in self.on_screen_keyboard:
        #     keys.update(letter, color)

        for guess in self.guesses:
            for letters in guess:
                if letters.bg_color != "#6aaa64" and letters.bg_color != "#c9b458":
                    letters.update_bg_color(letter, color)
        
        self.on_screen_keyboard.update_bg_color(letter, color)

        pygame.display.update()