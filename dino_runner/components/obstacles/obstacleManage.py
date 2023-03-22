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
            elif game.score > 300:
                self.obstacles.append(Bird(BIRD))

        self.num = random.randint(0, 1)

        for obstacles in self.obstacles:
            obstacles.update(game.game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacles.rect):

                # Verifica se tem algum poder ativado
                # Se estiver ativado, e não for o lucky_speed, o bloco não será execultado e o jogador pode tocar nos obstacles
                # Se estiver ativado, e for o lucky_speed, o bloco será execultado e o jogador perde se tocar no obstacle
                # Se estiver desativado e o jogador tocar, perde o jogo

                # Duas possibilidade de perder: tocando sem poder ou tocando com o lucky_speed
                if (not game.player.has_power_up) or (game.player.lucky_speed):

                    game.playing = False
                    pygame.time.delay(1500)
                    game.death_count += 1
                    break

                # Se o hammer estiver ativado os obstacles serão destruidos ao tocar o dino
                # se for Shield, os obstacles passaram pelo dino
                elif game.player.hammer == True:
                    self.obstacles.remove(obstacles)
                # se o shield estiver ativado, vai atravessar os obstacles
                
    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []