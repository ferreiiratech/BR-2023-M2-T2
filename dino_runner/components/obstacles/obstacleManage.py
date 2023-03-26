import pygame
import random

from dino_runner.utils.constants import *
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
            elif game.score > 10:
                self.obstacles.append(Bird(BIRD))

        self.num = random.randint(0, 1)

        for obstacles in self.obstacles:
            obstacles.update(game.game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacles.rect):
                if (not game.player.has_power_up) or (game.player.portal_speed):
                    pygame.mixer.music.stop()
                    SOUND_GAME_OVER.play()
                    pygame.time.delay(2500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.fire == True:
                    SOUND_FIRE.play()
                    self.obstacles.remove(obstacles)
                else:
                    SOUND_SHIELD.play()
                
    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []