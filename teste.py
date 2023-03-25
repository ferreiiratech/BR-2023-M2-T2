class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        # Posição y aleatória
        self.rect.y = random.randint(220, 325)
        self.index = 0

    def draw(self, screen):
        if self.index >= 10:
            self.index = 0
        # Trocar image do Bird
        screen.blit(self.image[self.index], self.rect)
        self.index += 1
