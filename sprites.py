import os
import time
import pygame
from random import choice

from settings import *


def tile_format(tile):
    tile = str(tile)

    if len(tile) == 1:
        tile = "000" + tile
    elif len(tile) == 2:
        tile = "00" + tile
    else:
        tile = "0" + tile

    return tile


def img_format(tile):
    return pygame.transform.scale(pygame.image.load(f'assets/img/tiles/tile_{tile}.png').convert_alpha(),
                                  (TILESIZE, TILESIZE))


class Character(pygame.sprite.Sprite):

    def __init__(self, game, color, x, y, speed):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.data()

        self.color = color

        self.key = False

        self.alive = True

        self.hp = PLAYER_HEALTH

        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['idle', 'run', 'jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'assets/img/player/{self.color}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.transform.scale(
                    pygame.image.load(f'assets/img/player/{self.color}/{animation}/{i}.png').convert_alpha(),
                    (TILESIZE, TILESIZE))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.moving_left = False
        self.moving_right = False

    def data(self):

        try:

            with open(FILES["money"], "r") as file:

                self.money = int(file.readline().strip())

        except FileNotFoundError:

            with open(FILES["money"], "w") as f:

                f.write("0")

                self.money = 0

    def move(self):

        screen_scroll = 0

        dx = 0
        dy = 0

        if self.moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -13
            self.jump = False
            self.in_air = True
            self.game.jump_sound.play()

        self.vel_y += GRAVITY
        dy += self.vel_y

        for tile in self.game.world.obstacle_list:

            dx, dy = self.collide(tile, dx, dy)

        for tile in self.game.slide_group:

            dx, dy = self.collide(tile, dx, dy)

        if pygame.sprite.spritecollide(self, self.game.river_group, False):
            self.hp -= 25

        for enemy in self.game.enemy_group:

            self.death(enemy)

        for danger in self.game.danger_group:

            self.death(danger)

        level_complete = False
        if pygame.sprite.spritecollide(self, self.game.exit_group, False) and self.key:
            self.game.win_sound.play()
            time.sleep(1.5)
            level_complete = True

        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
            dx = 0

        if self.rect.top + dy < 0:
            self.vel_y = 0
            dy = 0 - self.rect.top

        if self.rect.bottom + dy > HEIGHT:
            self.hp = 0

        if self.game.choose_level:
            dx = 0
            dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if ((self.rect.right > WIDTH - SCROLL and self.game.bg_scroll < self.game.world.length - WIDTH)
                or (self.rect.left < SCROLL and self.game.bg_scroll > abs(dx))):
            self.rect.x -= dx
            screen_scroll = -dx

        return screen_scroll, level_complete

    def death(self, object):

        if pygame.sprite.collide_mask(self, object):

            self.hp = 0
            dx = 0
            dy = 0
            self.game.hurt_sound.play()

    def collide(self, tile, dx, dy):

        if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
            dx = 0

        if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

            if self.vel_y < 0:

                if ((self.rect.right > tile.rect.left + 5) and not (self.rect.left > tile.rect.right - 5)) or \
                        (not (self.rect.right > tile.rect.left + 5) and (self.rect.left > tile.rect.right - 5)):
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top

            elif self.vel_y >= 0:

                if ((self.rect.right > tile.rect.left + 5) and not (self.rect.left > tile.rect.right - 5)) or \
                        (not (self.rect.right > tile.rect.left + 5) and (self.rect.left > tile.rect.right - 5)):
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile.rect.top - self.rect.bottom

        return dx, dy

    def animation(self):

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def movement(self, index):

        if index != self.action:
            self.action = index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def animate(self):

        if self.alive:

            if not self.game.choose_level:

                if self.in_air and (self.moving_left or self.moving_right):
                    self.movement(2)
                elif self.moving_left or self.moving_right:
                    self.movement(1)
                else:
                    self.movement(0)

            else:

                self.movement(0)

            self.game.screen_scroll, self.level_complete = self.move()
            self.game.bg_scroll -= self.game.screen_scroll

    def live(self):

        if self.hp <= 0:

            if pygame.sprite.spritecollide(self, self.game.river_group, False):
                self.game.river_sound.play()

            self.hp = 0
            self.speed = 0
            self.alive = False
            self.game.restart_game = True

    def update(self):

        self.animation()

        self.live()

    def draw(self):

        self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Item(pygame.sprite.Sprite):

    def __init__(self, game, type, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.item_type = type
        self.image = pygame.transform.scale(pygame.image.load(ITEMS[self.item_type]).convert_alpha(),
                                            (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self, player):

        self.rect.x += self.game.screen_scroll

        if pygame.sprite.collide_mask(self, player):

            if self.item_type == 'Coin':
                player.money += 1
                self.game.coin_sound.play()
            elif self.item_type == 'Gem':
                pass
            elif self.item_type == 'Key':
                player.key = True
                self.game.key_sound.play()

            self.kill()


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, tile, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img_format(tile_format(tile))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))


class Slide(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.tile = tile

        self.speed = SLIDES[self.tile]["speed"]
        self.direction = 1

        self.image = img_format(tile_format(self.tile))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

        self.position = self.rect.centerx

        self.moving_left = True
        self.moving_right = False

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self):

        if self.moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1

        if abs(self.rect.centerx - self.position) > TILESIZE * SLIDES[self.tile]["range"] and self.moving_left:

            dx = self.speed

            self.moving_left = False
            self.moving_right = True

        elif abs(self.rect.centerx - self.position) > TILESIZE * SLIDES[self.tile]["range"] and self.moving_right:

            dx = -self.speed

            self.moving_left = True
            self.moving_right = False

        self.rect.x += dx

    def update(self, player):

        self.move()

        self.rect.x += self.game.screen_scroll
        self.position += self.game.screen_scroll

        self.game.screen.blit(self.image, self.rect)


class Decoration(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.image = img_format(tile_format(tile))

        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self):
        self.rect.x += self.game.screen_scroll


class Exit(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.image = img_format(tile_format(tile))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self, player):
        self.rect.x += self.game.screen_scroll


class River(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.image = img_format(tile_format(tile))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self, player):
        self.rect.x += self.game.screen_scroll


class Danger(pygame.sprite.Sprite):

    def __init__(self, game, type, angle, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.type = type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        temp_list = []
        num_of_frames = len(os.listdir(f'assets/img/danger/{self.type}'))
        for i in range(num_of_frames):
            img = pygame.transform.scale(
                pygame.image.load(f'assets/img/danger/{self.type}/{i}.png').convert_alpha(),
                (TILESIZE, TILESIZE))
            temp_list.append(pygame.transform.rotate(img, angle))
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def animation(self):

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def movement(self, index):

        if index != self.action:
            self.action = index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def animate(self):

        self.movement(0)

    def update(self, player):

        if not self.game.choose_level:

            self.animation()

            self.animate()

        self.rect.x += self.game.screen_scroll


class Hazard(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.image = img_format(tile_format(tile))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self, player):

        self.rect.x += self.game.screen_scroll


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, type, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.type = type

        self.speed = ENEMIES[self.type]["speed"]
        self.direction = 1

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        temp_list = []
        num_of_frames = len(os.listdir(f'assets/img/enemy/{self.type}'))
        for i in range(num_of_frames):
            img = pygame.transform.scale(
                pygame.image.load(f'assets/img/enemy/{self.type}/{i}.png').convert_alpha(),
                (TILESIZE, TILESIZE))
            temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

        if self.type in SUSPENDED:
            self.rect.y += 2

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.position = self.rect.centerx

        if choice(["left", "right"]) == "left":
            self.moving_left = True
            self.moving_right = False
        else:
            self.moving_left = False
            self.moving_right = True

    def animation(self):

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def movement(self, index):

        if index != self.action:
            self.action = index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def animate(self):

        self.movement(0)

        self.move()

    def move(self):

        if self.moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1

        if abs(self.rect.centerx - self.position) > TILESIZE * ENEMIES[self.type]["range"] and self.moving_left:

            dx = self.speed
            self.moving_left = False
            self.moving_right = True

        elif abs(self.rect.centerx - self.position) > TILESIZE * ENEMIES[self.type]["range"] and self.moving_right:

            dx = -self.speed

            self.moving_left = True
            self.moving_right = False

        self.rect.x += dx

    def update(self, player):

        if not self.game.choose_level:

            self.animation()

            self.animate()

        self.rect.x += self.game.screen_scroll
        self.position += self.game.screen_scroll

        self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
