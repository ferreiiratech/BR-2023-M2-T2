import pygame
import random

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.num = 1

    def update(self, game):
        cactus_drawn = random.choice([SMALL_CACTUS, LARGE_CACTUS])

        if len(self.obstacles) == 0:
            if self.num:
                self.obstacles.append(Cactus(cactus_drawn))

            # pássaros só começam a aparecer com score acima de 300
            elif game.score > 100:
                self.obstacles.append(Bird(BIRD))
        self.num = random.randint(0, 1)
                
        for obstacles in self.obstacles:
            obstacles.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacles.rect):
                if not game.player.has_power_up:

                    game.playing = False
                    pygame.time.delay(1500)
                    
                    # Contador de morte
                    game.death_count += 1
                    break
                else:
                    self.obstacles.remove(obstacles)

    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []