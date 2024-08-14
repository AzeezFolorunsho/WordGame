import random
from wordle_plus_game.src.utils.word_files.words6 import WORDS6
from wordle_plus_game.src.utils.word_files.words5 import WORDS5
from wordle_plus_game.src.utils.word_files.words4 import WORDS4

class Random_word:
    def __init__(self):
        pass

    def get_random_word (self, length):
        if length == 4 or 5 or 6:
            if length == 4:
                return random.choice(WORDS4)
            elif length == 5:
                return random.choice(WORDS5)
            else:
                return random.choice(WORDS6)
        else:
            print("Invalid word length input")