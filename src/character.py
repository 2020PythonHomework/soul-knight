import pygame
from pygame.locals import * # 导入pygame中所有常量

class MySprite(pygame.sprite.Sprite):
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
        self.movement = False           # 控制是否移动
        self.direction = 0               # 向左为0，向右为1，控制动画播放
        self.velocity = [0.0, 0.0]      # 人物速度[v_x, v_y]


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
        if self.movement:
            self.X += self.velocity[0]
            self.Y += self.velocity[1]
            self.first_frame = self.direction * 4        # 向左走从0帧到3帧，向右4-7帧
            self.last_frame = self.first_frame + 3
        else:
            self.first_frame = self.last_frame          # 人物静止

    #load picture---------------------------------------------------------
    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = 1

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
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

        self.move()

class Hero0(MySprite):
    def __init__(self, target):
        MySprite.__init__(self, target)








