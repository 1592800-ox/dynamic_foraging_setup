import pygame
from screeninfo import get_monitors

TICK_TO_DISTANCE = 10
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINE = (105,117,34)
GREEN = (0,255,0)

BG_COLOR = BLACK
BLOCK_COLOR = GREEN

class Block_UI:
    def __init__(self) -> None:
        pygame.init()
        # monitor
        self.m = get_monitors()[1]
        self.window = pygame.display.set_mode((self.m.width, self.m.height), pygame.FULLSCREEN, display=1)
        self.window.fill((BG_COLOR))
        pygame.display.flip()
        self.rec_width = self.m.width / 5
        self.rec_height = self.m.height / 3
        self.x_pos = self.m.width / 2 - self.rec_width / 2
        self.y_pos = self.m.height / 2 - self.rec_height / 2
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.rec_width, self.rec_height)

    # move the block left a tick
    def update_left(self, in_trial):
        if in_trial:
            self.x_pos = self.x_pos - TICK_TO_DISTANCE
            if self.x_pos < 0 - self.rec_width:
                self.window.fill((BG_COLOR))
                pygame.display.flip()
                self.reset()
                return True
            else:
                return False
        else:
            return False
        
    def update_right(self, in_trial):
        if in_trial:
            self.x_pos = self.x_pos + TICK_TO_DISTANCE
            if self.x_pos > self.m.width:
                self.window.fill((BG_COLOR))
                pygame.display.flip()
                self.reset()
                return True
            else:
                return False
        else:
            return False
    
    def draw(self):
        self.window.fill((BG_COLOR))
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.rec_width, self.rec_height)
        pygame.draw.rect(self.window, BLOCK_COLOR, self.rect)
        pygame.display.flip()

    # reset would be called after a trial ends
    def reset(self) -> None:
        self.x_pos = self.m.width / 2 - self.rec_width / 2
        self.y_pos = self.m.height / 2 - self.rec_height / 2


Block_UI.__doc__ = 'Object controlling the onscreen display as well as choice identification'