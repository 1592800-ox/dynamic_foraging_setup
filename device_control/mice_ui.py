import pygame
from screeninfo import get_monitors

ANGLE_TO_DISTANCE = 1 / 1024
white = (255,255,255)
black = (0,0,0)

class Block_UI:
    def __init__(self) -> None:
        pygame.init()
        # monitor
        self.m = get_monitors()[0]
        self.window = pygame.display.set_mode((self.m.width, self.m.height))
        self.window.fill((black))
        self.rec_width = self.m.width / 5
        self.rec_height = self.m.height / 5
        self.x_pos = self.m.width / 2 - self.width / 2
        self.y_pos = self.m.height / 2 - self.height / 2
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    # move the block left a tick
    def update_left(self):
        self.x_pos = self.x_pos - ANGLE_TO_DISTANCE
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.draw()
        if self.x_pos < 0:
            self.reset()
            self.window.fill((black))
            return -1
        
    def update_right(self):
        self.x_pos = self.x_pos - ANGLE_TO_DISTANCE
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.draw()
        if self.x_pos > self.m.width:
            self.reset()
            self.window.fill((black))
            return 1
    
    def draw(self, win):
        pygame.draw.rect(win,(self.color, self.rect))
    
    def reset(self) -> None:
        self.velocity = 0
        self.x_pos = self.m.width / 2 - self.width / 2
        self.y_pos = self.m.height / 2 - self.height / 2
        return

    update_left.__doc__ = 'move the on screen block at a certain velocity'

Block_UI.__doc__ = 'Object controlling the onscreen display as well as choice identification'