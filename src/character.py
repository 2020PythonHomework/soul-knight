import pygame
from pygame.locals import * # 导入pygame中所有常量
import time
import random
import math

class MySprite(pygame.sprite.Sprite):
    player_velocity = [0,0]
    def __init__(self, target):
        # basic picture attributes-----------------------------------
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None               # 单帧图像
        self.master_image = None        # 精灵图序列
        self.rect = None                # 单帧相对于屏幕窗口位置、长宽, 控制该属性以控制人物位置
        self.topleft = 0,0
        self.frame = 0                  # 当前帧
        self.old_frame = -1             # 上一帧
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        #------------------------------------------------------
        # character message
        self.direction = 0  # 向左为0，向右为1，控制动画播放
        self.velocity = [0.0, 0.0]      # 人物速度[v_x, v_y]
        self.movement = False  # 控制是否移动

    #X property
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self):
        return self.rect.y
    def _sety(self, value):
        self.rect.y = value
    Y = property(_gety, _sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)

    #move character
    def move(self):
        if not self.movement:
            self.velocity[0] = self.velocity[1] = 0
        self.X += (self.velocity[0] - MySprite.player_velocity[0])
        self.Y += (self.velocity[1] - MySprite.player_velocity[1])
        self.first_frame = self.direction * self.columns        # 向左走从0帧到3帧，向右4-7帧
        self.last_frame = self.first_frame + self.columns - 1


    #load picture---------------------------------------------------------
    def load(self, filename, width, height, columns, birth_x=400, birth_y=300):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(birth_x,birth_y,width,height)
        self.columns = columns
       # rect = self.master_image.get_rect()
       # self.last_frame = 0

    #update picture-------------------------------------------------------
    def update(self, current_time, rate=100):
        # 循环播放动画
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame: # 是否更新图片
            frame_x = (self.frame % self.columns) * self.frame_width    # 帧左上x相对于master_image坐标
            frame_y = (self.frame // self.columns) * self.frame_height  # 帧左上y相对于master_image坐标
            subRect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(subRect)
            self.old_frame = self.frame

        self.move()

class Hero0(MySprite):
    def __init__(self, target):
        MySprite.__init__(self, target)
        # 初始化血、蓝
        self.__maxHp = 7
        self.currentHP = self.__maxHp
        self.__maxMp = 200
        self.currentMP = self.__maxMp
        self.velocity = MySprite.player_velocity
       # self.is_attack = False
        self.last_attack_time = 0
        self.attackCD = 0.2
    def can_attack(self):
        return (time.process_time() - self.last_attack_time > self.attackCD) \
               and self.currentMP > 0

    def attack(self, bullet_list, vel):
        return bullet_list.attack(self, vel)

    def show_state(self, screen):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)

        text = pygame.font.Font("1.ttf", 30)
        hp = text.render("HP", 3, WHITE)
        mp = text.render("MP", 3, WHITE)
        screen.blit(hp, (15, 0))
        screen.blit(mp, (15, 50))
        pygame.draw.rect(screen, WHITE, (70, 0, 200, 30), 4)
        pygame.draw.rect(screen, WHITE, (70, 50, 200, 30), 4)

        pygame.draw.rect(screen, RED, (73, 3, 195 * self.currentHP / self.__maxHp, 25), 0)
        pygame.draw.rect(screen, BLUE, (73, 53, 195 * self.currentMP / self.__maxMp, 25), 0)

        text0 = pygame.font.Font("1.ttf", 30)
        hp_n = text0.render(str(self.currentHP) + ' / ' + str(self.__maxHp), 10, WHITE)
        mp_n = text0.render(str(self.currentMP) + ' / ' + str(self.__maxMp), 10, WHITE)
        screen.blit(hp_n, (140, -2))
        screen.blit(mp_n, (115, 48))

    def update(self, current_time, rate=100):
        MySprite.update(self, current_time, rate)
        self.show_state(self.target_surface)



class Bullet(MySprite):
    def __init__(self, target, speed):
        MySprite.__init__(self, target)
        self.damage = 1
        self.__attackCD = 0.2
        self.speed = speed
        self.movement = True
    def is_out_screen(self):
        return self.X > 1080 or self.Y > 720 or self.X < 0 or self.Y < 0



class Bullet_list(object):
    def __init__(self, display_target, file, bullet_speed = 25):
        self.l = []
        self.l_pointer = 0

        for i in range(30):
            bullet = Bullet(display_target, bullet_speed)
            bullet.load(file, 40, 40, 1)
            self.l.append(bullet)
    def attack(self, owner, vel):
        # 初始化子弹位置、速度
        self.l[self.l_pointer].X = owner.X + 50
        self.l[self.l_pointer].Y = owner.Y + 50
        self.l[self.l_pointer].velocity = vel

        tmp = self.l[self.l_pointer]
        self.l_pointer = (self.l_pointer+1) % 30
        return tmp


class Monster0(MySprite):
    def __init__(self, target, bullet_list = None, bullet_group = None):
        MySprite.__init__(self, target)
        self.__maxHp = 10
        self.currentHP = self.__maxHp

        self.__attack_target = None
        self.bullet_list = bullet_list
        self.bullet_group = bullet_group
        self.max_stay_time = 1.5
        self.stay_start_time = 0
        self.stay_end_time = 0
        self.max_move_time = 1.5

        self.random_moveCD = 0.5
        self.random_move = 0

        self.attackCD = 0.4
        self.last_attack_time = 0

        self.reloadCD = 5
        self.attack_keep_time = 2
        self.attack_start_time = 0
        self.attack_stop_time = 0
        self.can_attack = False


        self.target_direction = [0,0]
        self.target_distance = 0

    def update(self, current_time, rate=100):
        MySprite.update(self, current_time, rate)
        x = self.attack_target.X - self.X
        y = self.attack_target.Y - self.Y
        self.target_distance = x*x + y*y
        if x != 0 or y != 0:

            self.target_direction[0] = x / math.sqrt(self.target_distance)
            self.target_direction[1] = y / math.sqrt(self.target_distance)
        else:
            self.target_direction = [0,0]
        #自动移动
        if self.movement == True and time.process_time() - self.random_move > self.random_moveCD:
            self.random_move = time.process_time()

            self.velocity[0] = 7 * self.target_direction[0]
            self.velocity[1] = 7 * self.target_direction[1]
            if self.velocity[0] > 0:
                self.direction = 1
            else:
                self.direction = 0

        if self.movement == False and (time.process_time() - self.stay_start_time > self.max_stay_time):
            self.movement = True
            self.stay_end_time = time.process_time()

        if self.movement == True and time.process_time() - self.stay_end_time > self.max_move_time:
            self.stay_start_time = time.process_time()
            self.movement = False
        # 自动移动代码结束------------------------------------------------
        # 自动开火
        if time.process_time() - self.attack_stop_time > self.reloadCD and self.can_attack == False:
            self.attack_start_time = time.process_time()
            self.can_attack = True
        if time.process_time() - self.attack_start_time > self.attack_keep_time and self.can_attack == True:
            self.attack_stop_time = time.process_time()
            self.can_attack = False

        if self.can_attack and time.process_time() - self.last_attack_time > self.attackCD:

            self.last_attack_time = time.process_time()
            x = self.target_direction[0] + random.uniform(-0.3,0.3)
            y = self.target_direction[1] + random.uniform(-0.3,0.3)
            if x != 0 or y != 0:
                x = x / math.sqrt(x*x + y*y)
                y = y/ math.sqrt(x*x + y*y)

            x = x * self.bullet_list.l[0].speed
            y = y * self.bullet_list.l[0].speed
            self.bullet_group.add(self.attack(self.bullet_list, [x, y] ))
        # 自动开火结束----------------------------------
        # 检测是否死亡并移除自身
        if self.currentHP <= 0:
            self.kill()


    @property
    def attack_target(self):
        return self.__attack_target
    @attack_target.setter
    def attack_target(self, target):
        self.__attack_target = target

    def attack(self, bullet_list, vel):
        return bullet_list.attack(self, vel)






