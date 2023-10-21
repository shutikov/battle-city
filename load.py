import pygame

player_image = [pygame.image.load('img/player/player 1.png').convert_alpha(),
                pygame.image.load('img/player/player 2.png').convert_alpha()]
player_bullet = pygame.image.load('img/player/player bullet.png').convert_alpha()
bullet_image = [pygame.image.load('img/player/1.png').convert_alpha(),
                pygame.image.load('img/player/2.png').convert_alpha(),
                pygame.image.load('img/player/3.png').convert_alpha(),
                pygame.image.load('img/player/4.png').convert_alpha()]
shot_sound=pygame.mixer.Sound('sound/shot.mp3')
boom_sound=pygame.mixer.Sound('sound/boom.mp3')
enemy_image = [pygame.image.load('img/enemy/enemy 1.png').convert_alpha(),
               pygame.image.load('img/enemy/enemy 2.png').convert_alpha()]
enemy_bullet = pygame.image.load('img/enemy/enemy bullet.png').convert_alpha()
brick_image = pygame.image.load('img/blocks/brick block.png').convert_alpha()
iron_image = pygame.image.load('img/blocks/iron block.png').convert_alpha()
bush_image = pygame.image.load('img/blocks/bush block.png').convert_alpha()
water_image = pygame.image.load('img/blocks/water block.png').convert_alpha()
flag_image = pygame.image.load('img/blocks/flag.png').convert_alpha()
button_image=pygame.image.load('img/button/button.png').convert_alpha()
