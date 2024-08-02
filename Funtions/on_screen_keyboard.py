import pygame
from Funtions.buttons import Text_Button

KEYS = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], 
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"], 
        ["Z", "X", "C", "V", "B", "N", "M"]]

class On_Screen_Keyboard:
    def __init__(self, x, y, font, bg_color):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.x_spacing = 20
        self.y_spacing = 40
        self.font = font
        self.text_color = "#FFFFFF"
        self.bg_color = bg_color
        self.button_width = 40
        self.button_height = 40
        # use list comprehention to generate alingment
        self.letter_key_list = [[Text_Button(key, self.font, self.text_color, self.bg_color, self.x, self.y, self.button_width, self.button_height) for key in KEYS[0]],
                                [Text_Button(key, self.font, self.text_color, self.bg_color, self.x, self.y, self.button_width, self.button_height) for key in KEYS[1]],
                                [Text_Button(key, self.font, self.text_color, self.bg_color, self.x, self.y, self.button_width, self.button_height) for key in KEYS[2]]]
        
        self.enter_key = Text_Button("Ent", self.font, self.text_color, self.bg_color, self.x, self.y, self.button_width * 3, self.button_height)
        self.delete_key = Text_Button("Del", self.font, self.text_color, self.bg_color, self.x, self.y, self.button_width * 2, self.button_height)

    # def generate_letter_key_list(self):
    #     for row in KEYS:
    #         for key in row:
    #             self.letter_key_list.append([Text_Button(key, self.font, self.text_color, self.bg_color, self.x, self.y, self.button_width, self.button_height) for key in row])

    def update(self, letter, color):
        # Updates the color of the indicator according to the guessed letter, and the input color.
        if self.text == letter.upper():
            self.bg_color = color
            self.draw()
    
    def align(self):
        # self.generate_letter_key_list()

        # Drawing the indicators on the screen.

        for rows in range (len(self.letter_key_list)):
            self.currnt_x = self.x
            self.currnt_y = self.y

            for key in range (len(self.letter_key_list[rows])):
                # sets the position of the button
                self.letter_key_list[rows][key].set_x_and_y(self.currnt_x, self.currnt_y)

                # moves x for next button in a row
                self.currnt_x += self.button_width + self.x_spacing
            
            # resets x and moves y for next row
            self.currnt_x = self.x
            self.currnt_y = self.button_height + self.y_spacing

            # indents row 2 to the right
            if rows == 0:
                self.currnt_x += self.button_width / 2
            
            # setting the position of the enter key
            if rows == 1:
                self.enter_key.set_x_and_y(self.currnt_x, self.currnt_y)
                self.currnt_x += self.enter_key.width + self.x_spacing

            if rows == 2:
                self.delete_key.set_x_and_y(self.currnt_x, self.currnt_y)

    def draw(self, screen):
        self.align()
        # Drawing all the letters on the screen.
        for rows in range (len(self.letter_key_list)):
            for key in range (len(self.letter_key_list[rows])):
                # draws the buttons and checks if the button was clicked, and returns the text of the button if so
                if self.letter_key_list[rows][key].draw(screen):
                    return self.letter_key_list[rows][key].text
        
        # draws the enter and delete keys, and checks if the button was clicked, and returns the text of the button if so
        if self.enter_key.draw(screen):
            return self.enter_key.text

        if self.delete_key.draw(screen):
            return self.delete_key.text