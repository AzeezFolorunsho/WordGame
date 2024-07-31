class BaseState:
    def __init__(self):
        self.next_state = None

    def handle_event(self, event):
        pass

    # def update(self):
    #     pass

    # def draw(self, screen):
    #     pass