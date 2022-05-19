import pygame
import toolbox
import os
import random

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")
sfx_folder = os.path.join(assets_folder, "sfx")


class PowerUp(pygame.sprite.Sprite):
    # функция конструктор
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.background_image = pygame.image.load(os.path.join(assets_folder, "powerupBackgroundBlue.png"))
        self.pick_power = random.randint(0, 3)
        if self.pick_power == 0:
            self.image = pygame.image.load(os.path.join(assets_folder, "powerupCrate.png"))
            self.power_type = "crate"
        if self.pick_power == 1:
            self.image = pygame.image.load(os.path.join(assets_folder, "powerupBarrel.png"))
            self.power_type = "barrel"
        if self.pick_power == 2:
            self.image = pygame.image.load(os.path.join(assets_folder, "powerupSplit.png"))
            self.power_type = "split"
            self.background_image = pygame.image.load(os.path.join(assets_folder, "powerupBackgroundRed.png"))
        if self.pick_power == 3:
            self.image = pygame.image.load(os.path.join(assets_folder, "powerupDrop.png"))
            self.power_type = "stream"
            self.background_image = pygame.image.load(os.path.join(assets_folder, "powerupBackgroundRed.png"))


        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.background_angle = 0
        self.spinny_speed = 2
        self.despawn_timer = 400

        self.sfx_pickup = pygame.mixer.Sound(os.path.join(sfx_folder, "powerup.wav"))

    def update(self, player):
        # столкновение с игроком
        if self.rect.colliderect(player.rect):
            self.sfx_pickup.play()
            player.powerUp(self.power_type)
            self.kill()

        # таймер на коробку
        self.despawn_timer -= 1
        if self.despawn_timer <= 0:
            self.kill()

        # автоповорот фона бонуса
        self.background_angle += self.spinny_speed
        bg_image_to_draw, bg_rect = toolbox.getRotatedImage(self.background_image, self.rect, self.background_angle)

        # управляем мирцанием бонусов (% - остаток от деления)
        if self.despawn_timer > 100 or self.despawn_timer % 10 > 5:
            self.screen.blit(bg_image_to_draw, bg_rect)
            self.screen.blit(self.image, self.rect)
