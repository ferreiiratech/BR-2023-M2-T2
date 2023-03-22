import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import *

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
JUNP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}


X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5


class Dinosaur(Sprite):
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.jump_vel = JUMP_VEL
        self.dino_jump = False
        self.dino_run = True
        self.dino_duck = False
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.show_text = False
        self.shield_time = 0

    def update(self, user_imput):
        if (user_imput[pygame.K_UP] or user_imput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
        elif user_imput[pygame.K_DOWN]:
            self.dino_duck = True
        elif not self.dino_jump or user_imput[pygame.K_DOWN]:
            self.dino_duck = False
            self.dino_jump = False
            self.dino_run = True
        
        if self.dino_run:
            self.run()
        
        if self.dino_jump:
            self.jump()
        
        if self.dino_duck and not self.dino_jump:
            self.duck()

        if self.step_index >= 9:
            self.step_index = 0

    def run_or_duck(self, VAR):
        self.image = VAR[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS + (35 if VAR == DUCK_IMG else 0)
        self.step_index += 1

    def run(self):
        self.run_or_duck(RUN_IMG)
        
    def jump(self):
        self.image = JUNP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
  
    def duck(self):
        self.run_or_duck(DUCK_IMG)
        
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y)) 