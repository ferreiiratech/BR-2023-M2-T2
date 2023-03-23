import random
from pygame.sprite import Sprite

from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH


class Cloud(Sprite):
    def __init__(self):
        self.image = CLOUD
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 250)
        self.image_width = CLOUD.get_width()

    def update(self, game_speed):
        self.rect.x -= game_speed/6

        if self.rect.x < self.rect.width - 200:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(100, 250)       

    def draw(self, screen):
        screen.blit(self.image, self.rect)