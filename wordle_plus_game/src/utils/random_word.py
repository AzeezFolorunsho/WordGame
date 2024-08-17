import random
from wordle_plus_game.src.utils.word_files.words6 import WORDS6
from wordle_plus_game.src.utils.word_files.words5 import WORDS5
from wordle_plus_game.src.utils.word_files.words4 import WORDS4

class RandomWord:
    def __init__(self):
        self.full_word_list = WORDS6 + WORDS5 + WORDS4

    def get_random_word (self, length):
        try:
            if length == 4 or 5 or 6:
                if length == 4:
                    return random.choice(WORDS4).lower()
                elif length == 5:
                    return random.choice(WORDS5).lower()
                else:
                    return random.choice(WORDS6).lower()
        except:
            print("Invalid word length input")