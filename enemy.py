import random

import pygame
import os
import toolbox
import math
from explosion import Explosion
from powerup import PowerUp

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")
sfx_folder = os.path.join(assets_folder, "sfx")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load(os.path.join(assets_folder, "Enemy_05.png"))
        self.image_hurt = pygame.image.load(os.path.join(assets_folder, "Enemy_05_hurt.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "MediumExplosion1.png")))
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "MediumExplosion2.png")))
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "MediumExplosion3.png")))
        self.angle = 0
        self.speed = 2
        self.health = 20
        self.hurt_timer = 0
        # урон при столкновении
        self.damage = 1
        # столкновение с коробкой
        self.obstacle = 0
        self.obstacle_max = 10
        self.powerup_chance = 10

        self.sfx_explode = pygame.mixer.Sound(os.path.join(sfx_folder, "explosion-small.wav"))

    def update(self, projectiles, crates, explosions):
        # вычисляем угол между игроком и противником
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)

        # двигаем противников в сторону игрока
        angle_rads = math.radians(self.angle)
        self.x_move = math.cos(angle_rads) * self.speed
        self.y_move = -math.sin(angle_rads) * self.speed

        # столкновение с коробками
        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move

        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x
                self.getAngry(crate)

        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y
                self.getAngry(crate)

        self.x = new_x
        self.y = new_y

        self.rect.center = (self.x, self.y)

        # проверяем столкновение со взрывом
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # проверяем столкновение снарядов с противником
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                # отнимаем здоровье у противника
                self.getHit(projectile.damage)
                # уничтожаем снаряд
                projectile.explode()

        # попадание по противнику - противник краснеет
        if self.hurt_timer <= 0:
            image_to_rotate = self.image
        else:
            image_to_rotate = self.image_hurt
            self.hurt_timer -= 1

        # поворот картинки
        self.image_to_draw, self.image_rect = toolbox.getRotatedImage(image_to_rotate, self.rect, self.angle)
        self.screen.blit(self.image_to_draw, self.image_rect)

    # функция попадания снаряда в противника
    def getHit(self, damage):
        self.hurt_timer = 5
        self.x -= self.x_move * 5
        self.y -= self.y_move * 5
        self.health -= damage
        if self.health <= 0:
            self.sfx_explode.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)
            #
            if random.randint(0, 100) < self.powerup_chance:
                PowerUp(self.screen, self.x, self.y)
            self.kill()
            self.player.getScore(1)


    # функция отсчета XP коробки
    def getAngry(self, crate):
        self.obstacle += 1
        if self.obstacle >= self.obstacle_max:
            crate.getHit(self.damage)
            self.obstacle = 0


class Enemy2(Enemy):
    def __init__(self, screen, x, y, player):
        Enemy.__init__(self, screen, x, y, player)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load(os.path.join(assets_folder, "Enemy_04.png"))
        self.image_hurt = pygame.image.load(os.path.join(assets_folder, "Enemy_05_hurt.png"))
        self.speed = 5
