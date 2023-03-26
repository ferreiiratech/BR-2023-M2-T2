import pygame
import json

from dino_runner.utils.constants import *
from dino_runner.components.goat import Goat
from dino_runner.components.obstacles.obstacleManage import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.clouds.cloud import Cloud


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
        self.x_pos_land = 0
        self.score = 0
        self.hi_score = 0
        self.scoreSaved = 0
        self.playerSaved = ""
        self.death_count = 0
        self.player_name = ""
        self.color_game = COLOR_WHITE
        self.color_text = COLOR_BLACK
        self.theme_dark = False
        self.landscape = LANDSCAPE1
        self.player = Goat()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.cloud = Cloud()

    def execute(self):
        self.running = True
        while self.running:
            self.music_game()
            if not self.playing:
                self.update_hi_score()
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def music_game(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.3)

    def run(self):
        self.reset_game()
        while self.playing:
            self.events_close()
            self.update()
            self.draw()
    
    def reset_game(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.player.has_power_up = False
        self.player.portal_speed = False
        self.score = 0
        self.game_speed = 20
        self.theme_dark = False

    def theme(self):
        if self.theme_dark:
            self.color_text = COLOR_WHITE
            self.color_game = COLOR_BLACK
            self.landscape = LANDSCAPE2
        else:
            self.color_text = COLOR_BLACK
            self.color_game = (13, 25, 41)
            self.landscape = LANDSCAPE1

    def events_close(self):
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
        self.cloud.update(self.game_speed)
        self.theme()

    def update_score(self):
        self.score += 1
        if self.score%100 == 0:
            self.game_speed += 1        

    def update_hi_score(self):
        with open('dino_runner/utils/save_score.json', 'r+') as arquivo:
            listaHiScore = json.loads(arquivo.read())
            
            if (self.score - 1) > listaHiScore[1]:
                arquivo.seek(0)
                listaHiScore = [self.player_name, self.score - 1]
                json.dump(listaHiScore, arquivo)
                arquivo.truncate()
                self.scoreSaved = self.score - 1
                self.playerSaved = self.player_name
            else:
                self.scoreSaved = listaHiScore[1]
                self.playerSaved = listaHiScore[0]
        arquivo.close()

    def requests_name(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player_name != '':
                    self.run()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode
        self.text_render("Name: " + self.player_name, COLOR_WHITE, FONT_STYLE, 20, (SCREEN_WIDTH//2, 400))

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(self.color_game)
        self.landscape_render()
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.screen_information()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        self.cloud.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        self.x_pos_bg -= self.game_speed
        
        image_width = FLOOR.get_width()
        self.screen.blit(FLOOR, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(FLOOR, (image_width + self.x_pos_bg, self.y_pos_bg))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(FLOOR, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0

    def landscape_render(self):
        if self.playing:
            self.x_pos_land -= self.game_speed/8

        y = -140

        self.screen.blit(self.landscape, (self.x_pos_land, y))

        image_width = self.landscape.get_width()
        self.screen.blit(self.landscape, (image_width + self.x_pos_land, y))

        if self.x_pos_land <= -image_width:
            self.screen.blit(self.landscape, (image_width + self.x_pos_land, y))
            self.x_pos_land = 0

    def text_render(self, message, color, fontText, size, position):
        font = pygame.font.Font(fontText, size)
        text = font.render(message, True, color)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def screen_information(self):
        messageScore = f"Score: {self.score}"
        position = (1000, 50)
        size = 22             
        self.text_render(messageScore, self.color_text, FONT_STYLE, size, position)

        messageSpeed = f"Speed: {self.game_speed}m/s"
        position = (100, 50)
        self.text_render(messageSpeed, self.color_text, FONT_STYLE, size, position)

        messageSpeed = f"HI: {self.scoreSaved}"
        position = (850, 50)
        self.text_render(messageSpeed, self.color_text, FONT_STYLE, size, position)

        messageSpeed = f"Player: {self.player_name}"
        position = (SCREEN_WIDTH//2, 50)
        self.text_render(messageSpeed, self.color_text, FONT_STYLE, size, position)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            
            if time_to_show >= 0:
                message = f"{self.player.type.capitalize()} enabled for {time_to_show} seconds"
                position = (SCREEN_WIDTH//2, 150)

                if self.player.portal_speed:
                    message = "SPEED has been reset"

                self.text_render(message, COLOR_WHITE, FONT_STYLE, 20, position)
            else:
                self.player.has_power_up = False

                if self.player.fire:
                    self.game_speed = 20

                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.player_name != '' and self.death_count > 0:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.run()
                        
    def show_menu(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            zoom_factor = .5
            zoomed_image = pygame.transform.scale(LANDSCAPE2, (LANDSCAPE2.get_width() * zoom_factor, LANDSCAPE2.get_height() * zoom_factor))
            self.screen.blit(zoomed_image, (SCREEN_WIDTH//7, SCREEN_HEIGHT//4))

            self.screen.blit(DINO_START, (half_screen_width - 48, half_screen_height - 100))

            messageStart = "Type your name and press enter to start"
            position = (half_screen_width, half_screen_height + 20)
            self.text_render(messageStart, COLOR_WHITE, FONT_STYLE, 22, position)

            self.requests_name()
        else:
            if self.theme_dark:
                self.screen.fill(self.color_game)
            else:
                self.screen.fill(COLOR_GRAY)
            self.screen.blit(GAME_OVER, (half_screen_width - 190, half_screen_height - 220))
            self.screen.blit(RESET, (half_screen_width - 25, half_screen_height - 50))

            messageReset = "Press the spacebar to restart"
            positionReset = (half_screen_width, half_screen_height - 120)
            self.text_render(messageReset, self.color_text, FONT_STYLE, 22, positionReset)
            
            messageScoreFinal = f"Score: {self.score - 1}   -   Death: {self.death_count}"
            positionScoreFinal = (half_screen_width , half_screen_height + 150)
            self.text_render(messageScoreFinal, self.color_text, FONT_STYLE, 22, positionScoreFinal)

            messageBestPlayer = f"Best player   -   {self.playerSaved.capitalize()}     HI Score   -   {self.scoreSaved}"
            positionBest = (half_screen_width , SCREEN_HEIGHT - 15)
            self.text_render(messageBestPlayer, self.color_text, FONT_STYLE, 18, positionBest)

        pygame.display.update()
        self.handle_events_on_menu()