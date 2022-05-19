import pygame
import os
import toolbox

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")


class HUD():
    # конструктор класса
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.hud_font = pygame.font.SysFont('default', 30)

        self.hud_font_big = pygame.font.SysFont('default', 80)
        self.score_text = self.hud_font.render('Score: 0', True, (255, 255, 255))

        self.start_timer_max = 50
        self.start_timer = self.start_timer_max

        # режим игры
        self.state = 'mainmenu'
        self.title_image = pygame.image.load(os.path.join(assets_folder, "title.png"))
        self.start_text = self.hud_font.render('Press any key to start', True, (255, 255, 255))

        # режим геймовер
        self.game_over_text = self.hud_font_big.render('GAME OVER', True, (255, 255, 255))
        self.reset_btn = pygame.image.load(os.path.join(assets_folder, "BtnReset.png"))

        # 1. загружаем иконки
        self.crate_icon = pygame.image.load(os.path.join(assets_folder, "Crate.png"))
        self.explosion_crate_icon = pygame.image.load(os.path.join(assets_folder, "ExplosiveBarrel.png"))
        self.split_shot_icon = pygame.image.load(os.path.join(assets_folder, "iconSplit.png"))
        self.stream_shot_icon = pygame.image.load(os.path.join(assets_folder, "iconStream.png"))
        self.normal_shot_icon = pygame.image.load(os.path.join(assets_folder, "Balloon.png"))

        # 2. создаем экземпляр класса AmmoTile - серый квадрат
        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosion_crate_ammo_tile = AmmoTile(self.screen, self.explosion_crate_icon, self.hud_font)
        self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)

    def update(self):
        # режим игры
        if self.state == 'ingame':
            # выводим счет
            self.score_text = self.hud_font.render('Score: ' + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.score_text, (10, 10))

            # 3. выводим обойму
            tile_x = 392
            self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
            tile_x += self.crate_ammo_tile.width
            self.explosion_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosion_crate_ammo)
            tile_x += self.explosion_crate_ammo_tile.width

            # вычисляем иконку для показа
            if self.player.shot_type == 'normal':
                self.balloon_ammo_tile.icon = self.normal_shot_icon
            elif self.player.shot_type == 'split':
                self.balloon_ammo_tile.icon = self.split_shot_icon
            elif self.player.shot_type == 'stream':
                self.balloon_ammo_tile.icon = self.stream_shot_icon

            self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.special_ammo)

        # режим главного меню
        elif self.state == 'mainmenu':

            # мирцание текста
            self.start_timer -= 1
            if self.start_timer <= 0:
                self.start_timer = self.start_timer_max

            title_x, title_y = toolbox.centerCoords(self.title_image, self.screen)
            self.screen.blit(self.title_image, (title_x, title_y))
            text_x, text_y = toolbox.centerCoords(self.start_text, self.screen)

            if self.start_timer > 30:
                self.screen.blit(self.start_text, (text_x, text_y + 150))

        # режим gameover
        elif self.state == 'gameover':
            title_x, title_y = toolbox.centerCoords(self.game_over_text, self.screen)
            self.screen.blit(self.game_over_text, (title_x, title_y))
            # выводим счет
            self.score_text = self.hud_font.render('Final score: ' + str(self.player.score), True, (255, 255, 255))
            title_x, title_y = toolbox.centerCoords(self.score_text, self.screen)
            self.screen.blit(self.score_text, (title_x, title_y + 40))
            # рисуем кнопку
            title_x, title_y = toolbox.centerCoords(self.reset_btn, self.screen)
            button_rect = self.screen.blit(self.reset_btn, (title_x, title_y + 150))

            # нажатие по кнопке Reset
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_position):
                        self.state = 'mainmenu'


class AmmoTile():
    # конструктор класса
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_image = pygame.image.load(os.path.join(assets_folder, "hudTile.png"))
        self.width = self.bg_image.get_width()

    def update(self, x, y, ammo):
        # выводим задний фон
        tile_rect = self.bg_image.get_rect()
        tile_rect.bottomleft = (x, y)
        self.screen.blit(self.bg_image, tile_rect)
        # выводим иконку
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)
        # выводим счет
        ammo_text = self.font.render(str(ammo), True, (255, 255, 255), (255, 0, 0))
        self.screen.blit(ammo_text, tile_rect.topleft)
