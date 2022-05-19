import pygame
import os
import toolbox
import math
from explosion import Explosion

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")
sfx_folder = os.path.join(assets_folder, "sfx")


class WaterBalloon(pygame.sprite.Sprite):
    # конструктор спрайта
    def __init__(self, screen, x, y, angle):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load(os.path.join(assets_folder, "BalloonSmall.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.speed = 10
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "SplashSmall1.png")))
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "SplashSmall2.png")))
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "SplashSmall3.png")))
        self.angle_rads = math.radians(self.angle)
        self.x_move = math.cos(self.angle_rads) * self.speed
        self.y_move = -math.sin(self.angle_rads) * self.speed
        # урон снаряда
        self.damage = 6

        self.sfx_splash = pygame.mixer.Sound(os.path.join(sfx_folder, "splash.wav"))

    def update(self):
        self.x += self.x_move
        self.y += self.y_move
        self.rect.center = (self.x, self.y)
        self.screen.blit(self.image, self.rect)

        # уничтожаем скрывшиеся пули
        if self.x < -self.image.get_width():
            self.kill()
        if self.x > self.screen.get_width() + self.image.get_width():
            self.kill()

    # функция уничтожения снаряда
    def explode(self):
        Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)
        self.sfx_splash.play()
        self.kill()


class WaterDroptel(WaterBalloon):
    # конструктор спрайта
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load(os.path.join(assets_folder, "DropSmall.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)