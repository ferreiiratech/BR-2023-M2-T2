import pygame

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacleManage import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

color_black = COLORS['black']
color_white = COLORS['white']
color_gray = COLORS['gray']
color_green = COLORS['green']


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()

        # Reset dos PowerUp's
        self.player.has_power_up = False
        self.player.lucky_speed = False

        self.score = 0
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_imput = pygame.key.get_pressed()
        self.player.update(user_imput)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score%100 == 0:
            self.game_speed += 1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(color_white)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        if self.playing:
            self.x_pos_bg -= self.game_speed
        
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        
    # criar um arquivo em utils para renderizar o texto
    def text_render(self, message, color, fontText, size, position):
        font = pygame.font.Font(fontText, size)
        text = font.render(message, True, color)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def draw_score(self):
        message = f"Score: {self.score}"
        position = (1000, 50)
        size = 22
        color = color_black

        if self.score%100 == 0:
            size = 40
            color = color_green                
            
        self.text_render(message, color, FONT_STYLE, size, position)
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            
            if time_to_show >= 0:
                message = f"{self.player.type.capitalize()} enabled for {time_to_show} seconds"
                color = COLORS['black']
                position = (SCREEN_WIDTH//2, 150)

                # se o poder ativado for lucky_speed teremos essa mensagem
                if self.player.lucky_speed:
                    message = "SPEED has been reset"
                    # color = ?

                self.text_render(message, color, FONT_STYLE, 20, position)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.run()

    def show_menu(self):
        self.screen.fill(color_white)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(DINO_START, (half_screen_width - 48, half_screen_height - 100))

            message = "Press the spacebar to play"
            position = (half_screen_width, half_screen_height + 20)
            self.text_render(message, color_black, FONT_STYLE, 22, position)
        else:
            self.screen.fill(color_gray)
            self.screen.blit(GAME_OVER, (half_screen_width - 190, half_screen_height - 220))
            self.screen.blit(RESET, (half_screen_width - 25, half_screen_height - 50))

            message = "Press the spacebar to restart"
            position = (half_screen_width, half_screen_height - 120)
            self.text_render(message, color_black, FONT_STYLE, 22, position)
            
            message1 = f"Score: {self.score - 1}   -   Death: {self.death_count}"
            position = (half_screen_width , half_screen_height + 150)
            self.text_render(message1, color_black, FONT_STYLE, 22, position)

            self.draw_background()

        pygame.display.update()
        self.handle_events_on_menu()


# Obrigatório:

# Implementação do HAMMER (destroi os obstacles) ✅

# Implementar PowerUp de sua escolha com funcionalidade diferente da que já existe ✅

# Melhorias no código

## Quina-feira Demo final, apresentar código completo
