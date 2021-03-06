import pygame
import os
from explosion import Explosion

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")
sfx_folder = os.path.join(assets_folder, "sfx")


class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load(os.path.join(assets_folder, "Crate.png"))
        self.image_hurt = pygame.image.load(os.path.join(assets_folder, "Crate_hurt.png"))
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "CrateRubble.png")))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 50
        self.hurt_timer = 0
        self.just_placed = True
        self.sfx_break = pygame.mixer.Sound(os.path.join(sfx_folder, "break.wav"))

    def update(self, projectiles, explosions):
        if not self.rect.colliderect(self.player.rect):
            self.just_placed = False

        # проверяем столкновение с пулями
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                projectile.explode()
                self.getHit(projectile.damage)

        # проверяем столкновение со взрывом
        for explosion in explosions:
            if self.rect.colliderect(explosion.rect):
                self.getHit(explosion.damage)

        # попадание в коробку
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            image_to_draw = self.image_hurt
        else:
            image_to_draw = self.image

        self.screen.blit(image_to_draw, self.rect)

    def getHit(self, damage):
        self.health -= damage
        self.hurt_timer = 5
        if self.health <= 0:
            self.health = 99999
            self.sfx_break.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 20, 7, False)
            self.kill()


class ExplosionCrate(Crate):
    def __init__(self, screen, x, y, player):
        Crate.__init__(self, screen, x, y, player)
        self.image = pygame.image.load(os.path.join(assets_folder, "ExplosiveBarrel.png"))
        self.image_hurt = pygame.image.load(os.path.join(assets_folder, "ExplosiveBarrel_hurt.png"))
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "LargeExplosion1.png")))
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "LargeExplosion2.png")))
        self.explosion_images.append(pygame.image.load(os.path.join(assets_folder, "LargeExplosion3.png")))
        self.health = 20
        self.sfx_explode = pygame.mixer.Sound(os.path.join(sfx_folder, "explosion-big.wav"))

    def getHit(self, damage):
        self.health -= damage
        self.hurt_timer = 5
        if self.health <= 0:
            self.health = 99999
            self.sfx_explode.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 7, True)
            self.kill()
