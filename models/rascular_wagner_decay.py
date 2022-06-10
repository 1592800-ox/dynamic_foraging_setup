# rascular wagner model with decaying
class RW_decay:
    def __init__(self) -> None:
        self.alpha = 0.5
        self.beta = 0.5
    
    def make_choice(self) -> int:
        