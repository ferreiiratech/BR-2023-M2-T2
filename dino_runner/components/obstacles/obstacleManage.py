import pygame
import random

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        # controla se vai aparecer Bird ou Cactus
        self.num = 1

    def update(self, game):
        # add lista com os cactos
        cactus_drawn = random.choice([SMALL_CACTUS, LARGE_CACTUS])

        if len(self.obstacles) == 0:
            if self.num:
                self.obstacles.append(Cactus(cactus_drawn))
            else:
                self.obstacles.append(Bird(BIRD))
        # sorteio 
        self.num = random.randint(0, 1)
                
        for obstacles in self.obstacles:
            obstacles.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacles.rect):
                pygame.time.delay(500)
                game.playing = False
                game.death_count += 1
                #game.game_speed = 20 add depois
                break

    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []