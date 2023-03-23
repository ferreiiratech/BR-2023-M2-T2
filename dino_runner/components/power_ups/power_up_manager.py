import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.lucky_speed import Lucky_speed
from dino_runner.utils.constants import *


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.num = 2

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
                         
            # só entra aqui se não tiver nenhum PowerUp na tela e se
            # o valor sorteado somado com o valor sorteado anteriormente
            # for igual ao score atual
            self.when_appears += random.randint(200, 300) # Mudar para (500, 1000) para ficar mais raro de aparecer

            if self.num == 0:
                self.power_ups.append(Shield())
            elif self.num == 1:
                self.power_ups.append(Hammer())
            elif score > 30:
                self.power_ups.append(Lucky_speed())

            self.num = 2 #random.randint(0, 2)

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                
                # Verifica qual class o power_up pertence
                # 1 pode por vez. Se pegar um, o outro desativa
                if isinstance(power_up, Shield):
                    game.player.shield = True
                    game.player.hammer = False
                    game.player.lucky_speed = False
                    SOUND_POWER_UP.play()
                elif isinstance(power_up, Hammer):
                    game.player.hammer = True
                    game.player.shield = False
                    game.player.lucky_speed = False
                    SOUND_POWER_UP.play()
                elif isinstance(power_up, Lucky_speed):
                    game.player.lucky_speed = True
                    game.player.shield = False
                    game.player.hammer = False
                    game.game_speed = 20
                    game.color_game = COLOR_BLACK
                    game.color_text = COLOR_WHITE
                    SOUND_POWER_UP.play()
                
                game.player.has_power_up = True
                game.player.type = power_up.type
                game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        # PowerUp só irá aparecer qnd jogador atingir uma pontuação sorteiada pelo randon entre 500 e 1000
        # Mudar para (500, 1000)
        self.when_appears = random.randint(200, 300)