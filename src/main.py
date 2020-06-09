#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'a note string'

import sys
import time
import pygame
from pygame.locals import *
#import core
from character import *

hero_png = '../img/character/hero.png'
map_bottom_png = '../img/map/back0.png'
map_top_png = '../img/map/shit.png'
windows_size = (640, 480)
pistol_png = '../img/weapons/pistol.png'


#main__--------------------------------------------------------------
pygame.init()
pygame.display.set_caption('soul knight')           # 标题设置
screen = pygame.display.set_mode(windows_size)      # 启动屏幕
framerate = pygame.time.Clock()                     # 控制游戏最大帧率

# initial player
hero0 = Hero0(screen)
hero0.load(hero_png, 100, 100, 4)
hero_group = pygame.sprite.Group()
hero_group.add(hero0)

# initial weapon
bullet_list = []
list_pointer = 0
for i in range(10):
    pistol = Bullet(screen)
    pistol.load(pistol_png, 40, 20, 2)
    bullet_list.append(pistol)
hero_bullet_group = pygame.sprite.Group()
# hero_bullet_group.add(pistol)

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()                 # pygame初始化以来至现在的毫秒数


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == KEYUP:
            hero0.movement = False
            hero0.velocity = [0,0]

    keys = pygame.key.get_pressed()

# 控制人物移动

    if keys[K_w]:
        hero0.velocity[1] = -5
        hero0.movement = True
    if keys[K_s]:
        hero0.velocity[1] = 5
        hero0.movement = True
    if keys[K_d]:
        hero0.velocity[0] = 5
        hero0.movement = True
        hero0.direction = 1
    if keys[K_a]:
        hero0.velocity[0] = -5
        hero0.movement = True
        hero0.direction = 0
    # 控制开火
    if (keys[K_j] or keys[K_k] or keys[K_l] or keys[K_i])\
            and time.process_time() - hero0.last_attack_time > hero0.atackCD:
        hero0.is_attack = True
        hero0.last_attack_time = time.process_time()
        bullet_list[list_pointer].X = hero0.X
        bullet_list[list_pointer].Y = hero0.Y
        bullet_list[list_pointer].velocity[0] = \
            bullet_list[list_pointer].speed * (keys[K_l] - keys[K_j])
        bullet_list[list_pointer].velocity[1] = \
            bullet_list[list_pointer].speed * (keys[K_k] - keys[K_i])
        hero_bullet_group.add(bullet_list[list_pointer])
        list_pointer = (list_pointer+1)%10

    # 清空飞出屏幕的子弹
    for i in range(10):
        if bullet_list[i].X > 640 or bullet_list[i].Y > 480\
                or bullet_list[i].X < 0 or bullet_list[i].Y < 0:
            hero_bullet_group.remove(bullet_list[i])
            print(i)
            bullet_list[i].position = hero0.position




    screen.fill((255,255,255))
    hero_group.update(ticks)
    hero_group.draw(screen)
    hero_bullet_group.update(ticks)
    hero_bullet_group.draw(screen)

    pygame.display.update()










