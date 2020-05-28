#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'a note string'

import sys
import pygame

hero_png = '../img/character/hero.png'
map_bottom_png = '../img/map/back0.png'
map_top_png = '../img/map/shit.png'

class Game:
    def __init__(self, title, width, height, fps=60):
        """
        :param title: 游戏窗口的标题
        :param width: 游戏窗口的宽度
        :param height: 游戏窗口的高度
        :param fps: 游戏每秒刷新次数
        """
        self.title = title
        self.width = width
        self.height = height
        self.screen_surf = None     #Surface对象（位图）
        self.fps = fps
        self.__init_pygame()
        self.__init_game()
        self.update()

    def __init_pygame(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen_surf = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()    # 用于控制游戏最大帧速率

    def __init_game(self):
        self.hero = pygame.image.load(hero_png).convert_alpha()
        self.map_bottom = pygame.image.load(map_bottom_png).convert_alpha()
        self.map_top = pygame.image.load(map_top_png).convert_alpha()

    def update(self):
        while True:
            self.clock.tick(self.fps)       # 控制每一次迭代后暂停时间
            # TODO:逻辑更新
            self.event_handler()
            # TODO:画面更新
            self.screen_surf.blit(self.hero, (100, 100))
            pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    Game("Soul knight", 640,480)








