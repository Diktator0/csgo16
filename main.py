import pygame
import os
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy, Enemy2
from crate import Crate
from explosion import Explosion
from crate import ExplosionCrate
from powerup import PowerUp
from hud import HUD

# настройки игры

pygame.init()
pygame.mixer.pre_init(buffer=1024)

game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# каталог с картинками
main_folder = os.path.dirname(__file__)
assets_folder = os.path.join(main_folder, "assets")

# подключаем фон игры
bg_img = pygame.image.load(os.path.join(assets_folder, "BG_Grass.png"))

# создаем группы для спрайтов
playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()
powerupGroup = pygame.sprite.Group()

# добавляем спрайты в группы
Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Enemy2.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionGroup
PowerUp.containers = powerupGroup

# создаем игрока и размещаем его в центре экрана
mr_player = Player(screen, game_width / 2, game_height / 2)

hud = HUD(screen, mr_player)

game_started = False


# Старт игры
def StartGame():
    global game_started
    global hud
    global mr_player

    hud.state = 'ingame'
    game_started = True

    mr_player.__init__(screen, game_width / 2, game_height / 2)

    for _ in range(10):
        ExplosionCrate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)


enemy_spawn_timer_max = 50
enemy_spawn_timer = 0

# ***************** Игровой цикл *****************
# Пока 'while running' код исполняется снова и снова
while running:
    # Прерываем игру по нажатию X или esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(bg_img, (0, 0))

    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                StartGame()
                break

    if game_started:
        # движение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            mr_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_d]:
            mr_player.move(1, 0, cratesGroup)
        if keys[pygame.K_w]:
            mr_player.move(0, -1, cratesGroup)
        if keys[pygame.K_s]:
            mr_player.move(0, 1, cratesGroup)
        # установка коробок
        if keys[pygame.K_SPACE]:
            mr_player.placeCrate()
            # StartGame()

        # [0] - левая клавиша мыши - стрельба
        if pygame.mouse.get_pressed()[0]:
            mr_player.shoot()

        # 2 - ПКМ установка взрывчатки
        if pygame.mouse.get_pressed()[2]:
            mr_player.placeExplosionCrate()

        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            a = random.randint(0, 1)
            if a > 0.9:
                new_enemy = Enemy2(screen, 0, 0, mr_player)
            else:
                new_enemy = Enemy(screen, 0, 0, mr_player)

            side_to_spawn = random.randint(0, 3)
            # top screen
            if side_to_spawn == 0:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = -new_enemy.image.get_height()
            # left screen
            elif side_to_spawn == 1:
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            # right screen
            elif side_to_spawn == 2:
                new_enemy.x = game_width + new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            else:
                # bottom screen
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = game_height + new_enemy.image.get_height()
            enemy_spawn_timer = enemy_spawn_timer_max

        # обновление всех спрайтов пули поочередно
        for projectile in projectilesGroup:
            projectile.update()

        # обновление всех врагов поочередно
        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, cratesGroup, explosionGroup)

        # обновляем ловушки
        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionGroup)

        # обновление взрыва
        for explosion in explosionGroup:
            explosion.update()

        # обновление powerUp
        for powerup in powerupGroup:
            powerup.update(mr_player)

        # обновление игрока
        mr_player.update(enemiesGroup, explosionGroup)

        # управляем режимом игры
        if not mr_player.alive:
            if hud.state == 'ingame':
                hud.state = 'gameover'
            elif hud.state == 'mainmenu':
                game_started = False
                playerGroup.empty()
                enemiesGroup.empty()
                projectilesGroup.empty()
                powerupGroup.empty()
                explosionGroup.empty()
                cratesGroup.empty()

    # выводим текст
    hud.update()

    # Обновляем экран
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))
