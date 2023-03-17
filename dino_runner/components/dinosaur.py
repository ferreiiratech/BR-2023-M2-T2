import pygame
from dino_runner.utils.constants import *


X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5

class Dinosaur:
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.jump_vel = JUMP_VEL
        self.dino_jump = False
        self.dino_run = True
        self.dino_duck = False

    def update(self, user_imput):

        if (user_imput[pygame.K_UP] or user_imput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True
        

        if user_imput[pygame.K_DOWN]:
            self.dino_duck = True

        if self.dino_run:
            self.run()
        
        if self.dino_jump:
            self.jump()
        
        if self.dino_duck:
            self.duck()



        if self.step_index >= 10:
            self.step_index = 0

    def run_or_duck(self, VAR):
        self.image = VAR[0] if self.step_index < 5 else VAR[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS + (35 if VAR == DUCKING else 0)
        self.step_index += .1 if VAR == DUCKING else 1

    def run(self):
        self.run_or_duck(RUNNING)
        
    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
        
    def duck(self):
        self.run_or_duck(DUCKING)
        if self.step_index > 5:
            self.dino_duck = False
    
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

        