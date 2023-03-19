import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        # Posição y aleatória
        self.rect.y = random.randint(220, 325)
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        # Pegando a divisão inteira por 5. Uma hora 0 outra hora 1
        # Trocar image do Bird
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1
