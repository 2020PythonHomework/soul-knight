#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'a note string'

import sys
import pygame
from pygame.locals import *
#import core
from character import MySprite

hero_png = '../img/character/hero.png'
map_bottom_png = '../img/map/back0.png'
map_top_png = '../img/map/shit.png'
windows_size = (640, 480)


#main__--------------------------------------------------------------
pygame.init()
pygame.display.set_caption('soul knight')           # 标题设置
screen = pygame.display.set_mode(windows_size)      # 启动屏幕
framerate = pygame.time.Clock()                     # 控制游戏最大帧率

# initial player
hero = MySprite(screen)
hero.load(hero_png, 100, 100, 4)
hero_group = pygame.sprite.Group()
hero_group.add(hero)

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()                 # pygame初始化以来至现在的毫秒数

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    hero_group.update(ticks)
    hero_group.draw(screen)
    pygame.display.update()










