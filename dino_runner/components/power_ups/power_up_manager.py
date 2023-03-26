import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.fire import Fire
from dino_runner.components.power_ups.portal_speed import Portal_speed
from dino_runner.utils.constants import *


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.num = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(500, 600)

            if self.num == 0:
                self.power_ups.append(Shield())
            elif self.num == 1:
                self.power_ups.append(Fire())
            elif score > 300:
                self.power_ups.append(Portal_speed())

            self.num = random.randint(0, 2)

    def update(self, game):
        
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                SOUND_POWER_UP.play()

                if isinstance(power_up, Shield):
                    game.player.shield = True
                    game.player.fire = False
                    game.player.portal_speed = False
                elif isinstance(power_up, Fire):
                    game.player.fire = True
                    game.player.shield = False
                    game.player.portal_speed = False
                    game.game_speed = 60
                elif isinstance(power_up, Portal_speed):
                    game.player.portal_speed = True
                    game.player.shield = False
                    game.player.fire = False
                    game.game_speed = 20

                    if game.theme_dark:
                        game.theme_dark = False
                    else:
                        game.theme_dark =  True

                game.player.has_power_up = True
                game.player.type = power_up.type
                game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)
    
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(500, 600)