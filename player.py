import pygame
import os
import toolbox
import projectile
from crate import Crate
from crate import ExplosionCrate

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")
sfx_folder = os.path.join(assets_folder, "sfx")


class Player(pygame.sprite.Sprite):
    # конструктор для создания спрайта игрока
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join(assets_folder, "Player_03.png"))
        self.image_hurt = pygame.image.load(os.path.join(assets_folder, "Player_03hurt.png"))
        self.image_death = pygame.image.load(os.path.join(assets_folder, "Enemy_01.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 8
        self.angle = 5
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 7  # перезарядка
        self.health_max = 30
        self.health = self.health_max
        self.health_bar_width = self.image.get_width()
        self.health_bar_height = 8
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)

        self.alive = True  # флаг жизни
        self.hurt_timer = 0

        self.crate_ammo = 10  # макс кол коробок
        self.explosion_crate_ammo = 10  # макс кол коробок
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10

        self.special_ammo = 0
        self.shot_type = 'normal'
        self.score = 0

        self.sfx_shot = pygame.mixer.Sound(os.path.join(sfx_folder, "shot.wav"))

    # обновление спрайта
    def update(self, enemies, explosions):
        self.rect.center = (self.x, self.y)

        # перезарядка оружия
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # перезарядка коробок
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1

        # проверка на столкновения со взрывом
        for explosion in explosions:
            if explosion.damage and explosion.damage_player:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # проверяем на столкновение с противником
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.getHit(0)
                self.getHit(enemy.damage)

        # получаем позицию мыши (x, y) и вычисляем угол для поворота
        if self.alive:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, mouse_x, mouse_y)

        # смена картинок
        if self.alive:
            if self.hurt_timer <= 0:
                image_to_rotate = self.image
            else:
                image_to_rotate = self.image_hurt
                self.hurt_timer -= 1
        else:
            image_to_rotate = self.image_death

        # поворот игрока
        image_to_draw, image_rect = toolbox.getRotatedImage(image_to_rotate, self.rect, self.angle)

        self.screen.blit(image_to_draw, image_rect)

        # Рисуем и перемещаем XP
        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft
        health_per = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_per
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255, 0), self.health_bar_green)

    # Движение спрайта
    def move(self, x_move, y_move, crates):
        if self.alive:
            test_rect = self.rect
            test_rect.x += self.speed * x_move
            test_rect.y += self.speed * y_move
            collision = False
            for crate in crates:
                if not crate.just_placed:
                    if test_rect.colliderect(crate.rect):
                        collision = True

            if not collision:
                self.x += self.speed * x_move
                self.y += self.speed * y_move

    # Стрельба
    def shoot(self):
        if self.alive:
            if self.shoot_cooldown <= 0:
                self.sfx_shot.play()
                # тип стрельбы
                if self.shot_type == 'normal':
                    projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
                elif self.shot_type == 'split':
                    projectile.WaterBalloon(self.screen, self.x, self.y, self.angle + 15)
                    projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
                    projectile.WaterBalloon(self.screen, self.x, self.y, self.angle - 15)
                    self.special_ammo -= 1
                elif self.shot_type == 'stream':
                    projectile.WaterDroptel(self.screen, self.x, self.y, self.angle)
                    self.special_ammo -= 1

                self.shoot_cooldown = self.shoot_cooldown_max

                if self.special_ammo <= 0:
                    self.powerUp('normal')

    # Столкновениеas
    def getHit(self, damage):
        if self.alive:
            self.hurt_timer = 5
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.alive = False

    # установка коробки
    def placeCrate(self):
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:
            Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max

    # установка коробки взрывчатки
    def placeExplosionCrate(self):
        if self.alive and self.explosion_crate_ammo > 0 and self.crate_cooldown <= 0:
            ExplosionCrate(self.screen, self.x, self.y, self)
            self.explosion_crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max

    # бонусы
    def powerUp(self, power_type):
        if power_type == "crate":
            self.crate_ammo += 10
        elif power_type == "barrel":
            self.explosion_crate_ammo += 10
        elif power_type == 'split':
            self.special_ammo = 39
            self.shot_type = 'split'
            self.shoot_cooldown_max = 7
        elif power_type == 'normal':
            self.shot_type = 'normal'
            self.shoot_cooldown_max = 10
        elif power_type == 'stream':
            self.shot_type = 'stream'
            self.special_ammo = 300
            self.shoot_cooldown_max = 3

    # подсчет очков
    def getScore(self, score):
        if self.alive:
            self.score += score
