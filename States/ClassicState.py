from .BaseState import BaseState
from ..WorldeClasicMain import play_classic

class ClassicState(BaseState):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        play_classic()