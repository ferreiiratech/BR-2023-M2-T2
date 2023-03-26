import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        # Posição y aleatória
        self.rect.y = random.choice([220, 230, 325])
        self.index = 0
        self.count = 0

    def draw(self, screen):
        if self.count == 2:
            self.index = (self.index + 1) % 37
            self.count = 0
        # Trocar image do Bird
        screen.blit(self.image[self.index], self.rect)
        self.count += 1

