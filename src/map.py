import pygame

from character import *
import random

# map-------------------------------------------------------
WALL_PNG = '../img/map/wall.png'
FLOUR_PNG = '../img/map/flour.png'
D_WALL_PNG = '../img/map/d_wall.png'
DOOR_PNG = '../img/map/door.png'


TILE_WIDTH = 100
TILE_HEIGHT =100


class MapBlock(MySprite):
    def __init__(self, target):
        MySprite.__init__(self, target)
        self.movement = True
    def move(self):
        if not self.movement:
            self.velocity[0] = self.velocity[1] = 0
        self.X += (self.velocity[0] - MySprite.player_velocity[0])
        self.Y += (self.velocity[1] - MySprite.player_velocity[1])




def load_map(filename):
    # 打开文本功能
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    max_width = max(map(len, level_map))
    level_map = list(map(lambda x: x.ljust(max_width, " "), level_map))
    return level_map

def generate_level(level, target_surface, wall_group, floor_group, door_group):
    #创建地图,精灵的函数
    for y in range(len(level)):
        for x in range(len(level[y])):
            block = MapBlock(target_surface)
            if level[y][x] == '.':
                block.load(FLOUR_PNG, 100, 100, 1, TILE_WIDTH*x, TILE_HEIGHT*y)
                floor_group.add(block)
            elif level[y][x] == '#' or level[y][x] == '%':
                block.load(WALL_PNG, 100, 100, 1, TILE_WIDTH*x, TILE_HEIGHT*y)
                wall_group.add(block)
            elif level[y][x] == 'd':
                block.load(DOOR_PNG, 100, 200, 1, TILE_WIDTH*x, TILE_HEIGHT*y - 100)
                door_group.add(block)

            elif level[y][x] == '@':
                block.load(WALL_PNG, 100, 100, 1, TILE_WIDTH * x, TILE_HEIGHT * y)
                wall_group.add(block)
                tmpx, tmpy = x, y
                # 计算房间长宽并储存在tmpxy中
                while tmpx <= len(level[y]):
                    if level[y][tmpx] != '%':
                        tmpx += 1
                    else:
                        tmpx = tmpx - x
                        break
                while tmpy <= len(level):
                    if level[tmpy][x] != '%':
                        tmpy += 1
                    else:
                        tmpy = tmpy - y
                        break
                r = Room(block, tmpx + 1, tmpy + 1)
                Room.room_list.append(r)

class Room(object):
    room_list = []
    def __init__(self, start_block, width, height):
        # 房间左上实时坐标及大小属性
        self.start_rect = start_block.rect
        self.width = width
        self.height = height
        self.__size = self.width * self.height
        # 本房间内怪物组
        self.monster_group = pygame.sprite.Group()
        self.max_monster_num = self.__size // 40

    def load_monster(self, filename, target_surface, bullet_list, bullet_group, attack_target, wall_group):
        for i in range(self.max_monster_num):
            monster = Monster0(target_surface, bullet_list, bullet_group)
            pos_x = random.randint(0, self.width-1)
            pos_y = random.randint(0, self.height-1)
            monster.load(filename, 100, 100, 4, self.X + 100 * pos_x, self.Y + 100*pos_y )
            monster.attack_target = attack_target
            self.monster_group.add(monster)


    @property
    def X(self):
        return self.start_rect.x

    @property
    def Y(self):
        return self.start_rect.y




