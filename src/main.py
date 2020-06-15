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
windows_size = (1080, 720)
pistol_png = '../img/weapons/pistol.png'
monster0_png = '../img/character/monster0.png'
bullet0_png = '../img/weapons/bullet0.png'
bullet1_png = '../img/weapons/bullet1.png'


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
hero_bl = Bullet_list(screen, bullet0_png)
hero_bullet_group = pygame.sprite.Group()

monster_bl = Bullet_list(screen, bullet1_png, bullet_speed=15)
monster_bullet_group = pygame.sprite.Group()
# initial a monster
monster0 = Monster0(screen, monster_bl, monster_bullet_group)
monster0.load(monster0_png, 100, 100, 4)
monster0.attack_target = hero0
monster_group = pygame.sprite.Group()
monster_group.add(monster0)



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
        hero0.velocity[1] = -7
        hero0.movement = True
    if keys[K_s]:
        hero0.velocity[1] = 7
        hero0.movement = True
    if keys[K_d]:
        hero0.velocity[0] = 7
        hero0.movement = True
        hero0.direction = 1
    if keys[K_a]:
        hero0.velocity[0] = -7
        hero0.movement = True
        hero0.direction = 0

    # 控制开火
    if (keys[K_j] or keys[K_k] or keys[K_l] or keys[K_i])\
            and hero0.can_attack():

        hero0.last_attack_time = time.process_time()        # 重置攻击CD
        hero_bullet_group.add(hero0.attack(hero_bl, [hero_bl.l[hero_bl.l_pointer].speed * (keys[K_l] - keys[K_j]),
                               hero_bl.l[hero_bl.l_pointer].speed * (keys[K_k] - keys[K_i])]))
        # mp减少
        hero0.currentMP -= 1




    # 清空飞出屏幕的子弹
    for i in hero_bl.l:
        if i.is_out_screen():
            hero_bullet_group.remove(i)
            i.position = hero0.position     # 避免子弹被清空后仍调用该函数

    # 检测玩家是否被击中
    attacker = pygame.sprite.spritecollideany(hero0, monster_bullet_group)
    if attacker != None:
        if pygame.sprite.collide_circle_ratio(0.65)(hero0, attacker):
            hero0.currentHP -= attacker.damage
            print(hero0.currentHP)
            monster_bullet_group.remove(attacker)



    screen.fill((255,255,255))
    hero_group.update(ticks)
    hero_group.draw(screen)
    hero_bullet_group.update(ticks)
    hero_bullet_group.draw(screen)
    monster_group.update(ticks)
    monster_group.draw(screen)
    monster_bullet_group.update(ticks)
    monster_bullet_group.draw(screen)

    pygame.display.update()










