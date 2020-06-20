import pygame
from pygame.locals import *
from character import *

# map-------------------------------------------------------
WALL_PNG = '../img/map/wall.png'
FLOUR_PNG = '../img/map/flour.png'
D_WALL_PNG = '../img/map/d_wall.png'


TILE_WIDTH = 100
TILE_HEIGHT =100

# tile_load_dict = {'#': ('../img/map/wall_png', False), '.': ('../img/map/flour.png', True)}
class MapBlock(MySprite):
    def __init__(self, target):
        MySprite.__init__(self, target)


def load_map(filename):
    # 打开文本功能
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    max_width = max(map(len, level_map))
    level_map = list(map(lambda x: x.ljust(max_width, " "), level_map))
    return level_map

def generate_level(level, target_surface, wall_group, floor_group):
    #创建地图,精灵的函数
    for y in range(len(level)):
        for x in range(len(level[y])):
            block = MapBlock(target_surface)
            if level[y][x] == '.':
                block.load(FLOUR_PNG, 100, 100, 1, TILE_WIDTH*x, TILE_HEIGHT*y)
                floor_group.add(block)
            elif level[y][x] == '#':
                block.load(WALL_PNG, 100, 100, 1, TILE_WIDTH*x, TILE_HEIGHT*y)
                wall_group.add(block)
