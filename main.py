import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
lvl = 'game'

from load import *


def lvlGame():
    sc.fill('black')
    brick_group.update()
    brick_group.draw(sc)
    bush_group.update()
    bush_group.draw(sc)
    iron_group.update()
    iron_group.draw(sc)
    water_group.update()
    water_group.draw(sc)
    enemy_group.update()
    enemy_group.draw(sc)
    player_group.update()
    player_group.draw(sc)
    flag_group.update()
    flag_group.draw(sc)
    bullet_player_group.update()
    bullet_player_group.draw(sc)
    pygame.display.update()


def drawMaps(nameFile):
    maps = []
    source = 'game lvl/' + str(nameFile)
    with open(source, 'r') as file:
        for i in range(0, 20):
            maps.append(file.readline().replace("\n", "").split(",")[0:-1])

    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 40
        for j in range(0, len(maps[0])):
            pos[0] = 40 * j
            if maps[i][j] == '1':
                water = Water(water_image, pos)
                water_group.add(water)
            elif maps[i][j] == '2':
                brick = Brick(brick_image, pos)
                brick_group.add(brick)
            elif maps[i][j] == '3':
                iron = Iron(iron_image, pos)
                iron_group.add(iron)
            elif maps[i][j] == '4':
                bush = Bush(bush_image, pos)
                bush_group.add(bush)
            elif maps[i][j] == '5':
                flag = Flag(flag_image, pos)
                flag_group.add(flag)
            elif maps[i][j] == '6':
                enemy = Enemy(enemy_image, pos)
                enemy_group.add(enemy)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.timer_shot = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 4
        self.dir = "top"

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.image = pygame.transform.rotate(player_image, 90)
            self.rect.x -= self.speed
            self.dir = "left"
        elif key[pygame.K_w]:
            self.image = pygame.transform.rotate(player_image, 0)
            self.rect.y -= self.speed
            self.dir = "top"
        elif key[pygame.K_d]:
            self.image = pygame.transform.rotate(player_image, 270)
            self.rect.x += self.speed
            self.dir = "right"
        elif key[pygame.K_s]:
            self.image = pygame.transform.rotate(player_image, 180)
            self.rect.y += self.speed
            self.dir = "bottom"
        self.timer_shot += 1
        if key[pygame.K_SPACE] and self.timer_shot / FPS > 1:
            bullet = Bullet_player(player_bullet, self.rect.center, self.dir)
            bullet_player_group.add(bullet)
            self.timer_shot = 0


class Bullet_player(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = 5

    def update(self):
        if self.dir == 'top':
            self.rect.y -= self.speed
        elif self.dir == 'bottom':
            self.rect.y += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed


class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = 5

    def update(self):
        if self.dir == 'top':
            self.rect.y -= self.speed
        elif self.dir == 'bottom':
            self.rect.y += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 1
        self.dir = 'top'
        self.timer_move = 0

    def update(self):
        self.timer_move += 1
        if self.timer_move / FPS > 2:
            if random.randint(1, 4) == 1:
                self.dir = 'top'
        if self.dir == "left":
            self.image = pygame.transform.rotate(enemy_image, 90)
            self.rect.x -= self.speed
        elif self.dir == "top":
            self.image = pygame.transform.rotate(enemy_image, 0)
            self.rect.y -= self.speed
        elif self.dir == "right":
            self.image = pygame.transform.rotate(enemy_image, 270)
            self.rect.x += self.speed
        elif self.dir == "bottom":
            self.image = pygame.transform.rotate(enemy_image, 180)
            self.rect.y += self.speed
        if pygame.sprite.spritecollide(self, brick_group, False):
            self.timer_move = 0
            if self.dir == 'top':
                self.dir = 'bottom'



class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top
            if player.dir == "top":
                player.rect.top = self.rect.bottom
        pygame.sprite.groupcollide(bullet_player_group, brick_group, True, True)

        if pygame.sprite.spritecollide(self, enemy_group, False):
            if enemy.dir == "left":
                enemy.rect.left = self.rect.right
            if enemy.dir == "right":
                enemy.rect.right = self.rect.left
            if enemy.dir == "bottom":
                enemy.rect.bottom = self.rect.top
            if enemy.dir == "top":
                enemy.rect.top = self.rect.bottom


class Bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Iron(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top
            if player.dir == "top":
                player.rect.top = self.rect.bottom
        pygame.sprite.groupcollide(bullet_player_group, iron_group, True, False)

        if pygame.sprite.spritecollide(self, enemy_group, False):
            if enemy.dir == "left":
                enemy.rect.left = self.rect.right
            if enemy.dir == "right":
                enemy.rect.right = self.rect.left
            if enemy.dir == "bottom":
                enemy.rect.bottom = self.rect.top
            if enemy.dir == "top":
                enemy.rect.top = self.rect.bottom


class Water(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top
            if player.dir == "top":
                player.rect.top = self.rect.bottom

        if pygame.sprite.spritecollide(self, enemy_group, False):
            if enemy.dir == "left":
                enemy.rect.left = self.rect.right
            if enemy.dir == "right":
                enemy.rect.right = self.rect.left
            if enemy.dir == "bottom":
                enemy.rect.bottom = self.rect.top
            if enemy.dir == "top":
                enemy.rect.top = self.rect.bottom


class Flag(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top
            if player.dir == "top":
                player.rect.top = self.rect.bottom
        pygame.sprite.groupcollide(bullet_player_group, flag_group, True, True)

        if pygame.sprite.spritecollide(self, enemy_group, False):
            if enemy.dir == "left":
                enemy.rect.left = self.rect.right
            if enemy.dir == "right":
                enemy.rect.right = self.rect.left
            if enemy.dir == "bottom":
                enemy.rect.bottom = self.rect.top
            if enemy.dir == "top":
                enemy.rect.top = self.rect.bottom


brick_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()
iron_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
bullet_player_group = pygame.sprite.Group()
player = Player(player_image, (200, 640))
player_group.add(player)
enemy = Enemy(player_image, (850, 150))
enemy_group.add(enemy)

drawMaps('1.txt')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl == 'game':
        lvlGame()
        clock.tick(FPS)
