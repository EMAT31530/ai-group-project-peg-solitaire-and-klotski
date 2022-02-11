#coding=gbk

import copy
import pygame
import random
from pygame.locals import *
#from gameobjects.vector2 import *
from sys import exit
from datas import chrs
from ksolution import ksolute

# 资源路径
bgimg = './res/new_bg.png'
blenderimg = './res/blender.png'
cherrsimg = './res/cherrs.png'
logoimg = './res/klotski.png'
kingimg = './res/king.png'
vleaderimg = './res/vleader.png'
hleaderimg = './res/hleader.png'
pawnimg = './res/pawn.png'
prebtnimg = './res/pre_button.png'
nextbtnimg = './res/next_button.png'
startbtnimg = './res/start_button.png'
answerbtnimg = './res/answer_button.png'
resetimg = './res/reset_button.png'
homeimg = './res/home_button.png'
undoimg = './res/undo_button.png'
pauseimg = './res/pause_button.png'
playimg = './res/play_button.png'
bgsound = './res/journey.mp3'
htsound = './res/p.wav'
wasound = './res/wa.wav'

# 棋局数据宏定义
# 对于多格角色，只有左上角格用K、H、V，其他占位格用S
# 如K在数组中表示为：K S
#                    S S
K = 7       # king，棋局中的'曹操'
H = 2       # 长度为2的横向元素，棋局中的横向大将
V = 3       # 长度为2的纵向元素，棋局中的纵向大奖
P = 4       # 长宽都为1的元素，棋局中的小兵
B = 0       # 长度都为1的空白位置
S = 1       # 多个角色的占位格

# 棋格宽高、棋盘左、上保留区、Blender位置
WID = 100
HID = 100
LM = 10
TM = 10
BLD_x = 10
BLD_y = 160
TIPS_POS = (210, 210)
TIME_POS = (14, 518)
STEP_POS = (360, 518)
RESET_POS = (110, 520)
HOME_POS = (185, 520)
UNDO_POS = (260, 520)

# 反方向定义
redest_dic = {
        'up' : 'down',
        'down' : 'up',
        'left' : 'right',
        'right' : 'left',
        }

# 角色与图片对应关系
t2img_dict = { 
        K:kingimg, H:hleaderimg,
        V:vleaderimg, P:pawnimg
        }

# 角色类
class Elet(object):

    # 角色的宽高格数
    tsize = { K:(2, 2), H:(2, 1), V:(1, 2), P:(1, 1)}
    
    # 初始化
    # target : 对应的surface
    # type ：角色类型，数字2、3、4、7，意义见上文宏定义
    # loct : 逻辑位置，整个棋盘为5x4矩阵，loct为矩阵行列，如(0, 2)表示第一行第三列
    # kboard ：当前棋局数据，为一个二维数组，意义见'棋局数据宏定义'
    def __init__(self, target, type, loct, kboard):
        self.surface = target
        self.type = type
        self.kboard = kboard
        self.loct = loct
        self.image = pygame.image.load(t2img_dict[type]).convert_alpha()
    
    # 序列化，用于打印显示
    def __str__(self):
        dic = {2:'H', 3:'V', 4:'P', 7:'K', 1:'S', 0:'B'}
        return 'type:%s loct:(%d, %d)' % (dic[self.type], self.loct[0], self.loct[1])

    # 在surface上绘制角色
    def draw(self):
        x, y = self.loct[1] * WID + LM, self.loct[0] * HID + TM
        self.surface.blit(self.image, (x, y))

    # 判断某坐标点是否在角色范围内
    def is_over(self, pos, WID=100, HID=100):
        x, y = self.loct[1] * WID + LM, self.loct[0] * HID + TM
        w, h = self.tsize[self.type][0]*WID, self.tsize[self.type][1]*HID
        return (x <= pos[0] < x + w) and (y <= pos[1] < y + h)

    # 将角色向某方向移动一格
    # dest : 方向，取值为'up', 'left', 'right', 'down'
    def move_once(self, dest):
        # 先判断能否移动，不能则返回
        if not self.can_move(dest):
            return 

        # 移动角色
        if self.type == K:
            if dest == 'up':
                self.kboard[self.loct[0]-1][self.loct[1]:self.loct[1]+2] = [K, S]
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+2] = [S, S]
                self.kboard[self.loct[0]+1][self.loct[1]:self.loct[1]+2] = [B, B]
                self.loct[0] -= 1
            if dest == 'down':
                self.kboard[self.loct[0]+1][self.loct[1]:self.loct[1]+2] = [K, S]
                self.kboard[self.loct[0]+2][self.loct[1]:self.loct[1]+2] = [S, S]
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+2] = [B, B]
                self.loct[0] += 1
            if dest == 'left':
                self.kboard[self.loct[0]][self.loct[1]-1:self.loct[1]+1] = [K, S]
                self.kboard[self.loct[0]+1][self.loct[1]-1:self.loct[1]+1] = [S, S]
                self.kboard[self.loct[0]][self.loct[1]+1] = B
                self.kboard[self.loct[0]+1][self.loct[1]+1] = B
                self.loct[1] -= 1
            if dest == 'right':
                self.kboard[self.loct[0]][self.loct[1]+1:self.loct[1]+3] = [K, S]
                self.kboard[self.loct[0]+1][self.loct[1]+1:self.loct[1]+3] = [S, S]
                self.kboard[self.loct[0]][self.loct[1]] = B
                self.kboard[self.loct[0]+1][self.loct[1]] = B
                self.loct[1] += 1
        if self.type == V:
            if dest == 'up':
                self.kboard[self.loct[0]-1][self.loct[1]] = V
                self.kboard[self.loct[0]][self.loct[1]] = S
                self.kboard[self.loct[0]+1][self.loct[1]] = B
                self.loct[0] -= 1
            if dest == 'down':
                self.kboard[self.loct[0]+1][self.loct[1]] = V
                self.kboard[self.loct[0]+2][self.loct[1]] = S
                self.kboard[self.loct[0]][self.loct[1]] = B
                self.loct[0] += 1
            if dest == 'left':
                self.kboard[self.loct[0]][self.loct[1]-1:self.loct[1]+1] = [V, B]
                self.kboard[self.loct[0]+1][self.loct[1]-1:self.loct[1]+1] = [S, B]
                self.loct[1] -= 1
            if dest == 'right':
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+2] = [B, V]
                self.kboard[self.loct[0]+1][self.loct[1]:self.loct[1]+2] = [B, S]
                self.loct[1] += 1
        if self.type == H:
            if dest == 'up':
                self.kboard[self.loct[0]-1][self.loct[1]:self.loct[1]+2] = [H, S]
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+2] = [B, B]
                self.loct[0] -= 1
            if dest == 'down':
                self.kboard[self.loct[0]+1][self.loct[1]:self.loct[1]+2] = [H, S]
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+2] = [B, B]
                self.loct[0] += 1
            if dest == 'left':
                self.kboard[self.loct[0]][self.loct[1]-1:self.loct[1]+2] = [H, S, B]
                self.loct[1] -= 1
            if dest == 'right':
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+3] = [B, H, S]
                self.loct[1] += 1
        if self.type == P:
            if dest == 'up':
                self.kboard[self.loct[0]-1][self.loct[1]] = P
                self.kboard[self.loct[0]][self.loct[1]] = B
                self.loct[0] -= 1
            if dest == 'down':
                self.kboard[self.loct[0]+1][self.loct[1]] = P
                self.kboard[self.loct[0]][self.loct[1]] = B
                self.loct[0] += 1
            if dest == 'left':
                self.kboard[self.loct[0]][self.loct[1]-1:self.loct[1]+1] = [P, B]
                self.loct[1] -= 1
            if dest == 'right':
                self.kboard[self.loct[0]][self.loct[1]:self.loct[1]+2] = [B, P]
                self.loct[1] += 1

    # 判断角色是否能向某个方向移动
    # dest : 方向，取值为'up', 'left', 'right', 'down'
    def can_move(self, dest):
        if (dest == 'up') and (self.loct[0] > 0):
            if (self.type in (P, V)) and (self.kboard[self.loct[0]-1][self.loct[1]] == B):
                return True
            if (self.type in (K, H)) and (self.kboard[self.loct[0]-1][self.loct[1]] == B) and \
               (self.kboard[self.loct[0]-1][self.loct[1]+1] == B):
                return True

        if (dest == 'down') and (self.loct[0] + self.tsize[self.type][1] < 5):
            if (self.type in (P, V)) and (self.kboard[self.loct[0]+self.tsize[self.type][1]][self.loct[1]] == B):
                return True
            if (self.type in (K, H)) and (self.kboard[self.loct[0]+self.tsize[self.type][1]][self.loct[1]] == B) and \
               (self.kboard[self.loct[0]+self.tsize[self.type][1]][self.loct[1] + 1] == B):
                return True

        if (dest == 'left') and (self.loct[1] > 0):
            if (self.type in (P, H)) and (self.kboard[self.loct[0]][self.loct[1]-1] == B):
                return True
            if (self.type in (K, V)) and (self.kboard[self.loct[0]][self.loct[1]-1] == B) and \
               (self.kboard[self.loct[0]+1][self.loct[1]-1] == B):
                return True

        if (dest == 'right') and (self.loct[1] + self.tsize[self.type][0] < 4):
            if (self.type in (P, H)) and (self.kboard[self.loct[0]][self.loct[1]+self.tsize[self.type][0]] == B):
                return True
            if (self.type in (K, V)) and (self.kboard[self.loct[0]][self.loct[1]+self.tsize[self.type][0]] == B) and \
               (self.kboard[self.loct[0]+1][self.loct[1]+self.tsize[self.type][0]] == B):
                return True

        return False

# 棋局类
class Aspect():
    
    def __init__(self, target):
        self.surface = target
        self.kboard = None
        self.elets = []

    # 从一个二维数组生成棋局
    def load_board(self, pdata):
        self.clear()
        self.kboard = copy.deepcopy(pdata)
        for r in range(5):
            for c in range(4):
                if pdata[r][c] in (K, V, H, P):
                    e = Elet(self.surface, pdata[r][c], [r,c], self.kboard)
                    self.elets.append(e)

    # 绘制棋局元素
    def draw(self):
        for e in self.elets:
            e.draw()

    # 打印棋局
    def display(self):
        dic = {2:'H', 3:'V', 4:'P', 7:'K', 1:'S', 0:'B'}
        for r in self.kboard:
            rs = [dic[i] for i in r]
            print(' '.join(rs))
        print('')

    # 判断结束
    def is_finished(self):
        for e in self.elets:
            if (e.type == K) and (e.loct == [3, 1]):
                return True
        return False

    # 返回棋局数据(不含角色元素)
    def get_data(self):
        return self.kboard

    # 清空棋局
    def clear(self):
        self.kboard = None
        self.elets = []

# 按钮类
class Button(object):
    def __init__(self, image_filename, position):
        self.pos = position
        self.image = pygame.image.load(image_filename)

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    # 如果point在自身范围内，返回True
    def is_over(self, pos):
        pos_x, pos_y = pos
        x, y = self.pos
        w, h = self.image.get_size()
        return (x < pos_x <= x+w) and (y < pos_y <= y+h)

# 播放/暂停按钮类
class PlayPauseButton(Button):
    def __init__(self, pauseimg, playimg, position):
        Button.__init__(self, pauseimg, position)
        self.pauseimg = pauseimg
        self.playimg = playimg
        self.status = True

    def reverse(self):
        if self.status:
            self.image = pygame.image.load(self.playimg)
            self.status = False
        else:
            self.image = pygame.image.load(self.pauseimg)
            self.status = True
    
    def get_status(self):
        return self.status

# 一个精灵类, 飞舞的爱心，用于过关庆祝
class lover(pygame.sprite.Sprite):
    def __init__(self, target, image):
        pygame.sprite.Sprite.__init__(self)
        self.surface = target
        self.image = pygame.image.load(image).convert_alpha()
        self.rect  = self.image.get_rect()
        self.x = random.randint(0,target.get_width())   #初始化爱心横坐标
        self.y = random.randint(0,target.get_height())  #初始化爱心纵坐标
        self.vx= random.randint(-3,3)                   #初始化横向速度
        self.vy= random.randint(1,3)                    #初始化纵向速度
        self.rect.center = (self.x, self.y)

    def update(self):
        w, h = self.surface.get_size()
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

        if (self.x<=0) or (self.x>=h):
            self.vx *= -1

        if (self.y>=h):
            self.y = 0

def main():
    # 初始化音频参数
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    # 初始化pygame参数
    pygame.init()

    # 创建定时器
    clock  = pygame.time.Clock()

    # 创建窗口
    screen = pygame.display.set_mode((420, 563), 0)

    # 加载并转换背景
    background = pygame.image.load(bgimg).convert_alpha()
    blender = pygame.image.load(blenderimg).convert_alpha()
    cherrs = pygame.image.load(cherrsimg).convert_alpha()
    logo = pygame.image.load(logoimg)

    # 设置标题
    pygame.display.set_caption(u"Klotski")

    # 设置图标
    pygame.display.set_icon(logo)

    # 创建定时器事件
    ONESECOND = USEREVENT + 1
    pygame.time.set_timer(ONESECOND, 1000)
    TWOSECOND = USEREVENT + 2
    pygame.time.set_timer(TWOSECOND, 0)

    # 加载字体
    font = pygame.font.Font("./res/msyh.ttf", 35)
    sfont = pygame.font.Font("./res/msyh.ttf", 24)

    # 创建一个精灵组
    group = pygame.sprite.Group()
    # 爱心图像文件列表
    fimages = ['res/star1.png', 'res/star2.png', 'res/star3.png']
    # 建立80个爱心精灵
    for i in range(80):
        index = random.randint(0, 2)
        lstar = lover(screen, fimages[index])
        group.add(lstar)

    # 创建棋局
    chessp = Aspect(screen)

    # 棋库索引
    cpinx = 0

    # 棋局选择界面的按钮
    buttons = {}
    buttons['pre'] = Button(prebtnimg, (BLD_x, BLD_y))
    buttons['next'] = Button(nextbtnimg, (BLD_x+320, BLD_y))
    buttons['start'] = Button(startbtnimg, (BLD_x, BLD_y+60))
    buttons['answer'] = Button(answerbtnimg, (BLD_x+200, BLD_y+60))

    # 走棋过程中的按钮
    playbtns = {}
    playbtns['reset'] = Button(resetimg, RESET_POS)
    playbtns['home'] = Button(homeimg, HOME_POS)
    playbtns['undo'] = Button(undoimg, UNDO_POS)

    # 解密过程中的按钮
    answerbtns = {}
    answerbtns['play'] = PlayPauseButton(pauseimg, playimg, RESET_POS)
    answerbtns['home'] = Button(homeimg, HOME_POS)
    answerbtns['undo'] = Button(undoimg, UNDO_POS)

    # 开始循环
    while True:
        # 运行模式，0:选择棋局 1:走棋 2:解密
        run_mode = 0

        # 棋局选择阶段，选择完后可以开始或解密
        while run_mode == 0:
            button_pressed = None

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    # 判断哪个按钮被按下
                    for button_name, button in buttons.iteritems():
                        if button.is_over(event.pos):
                            print (button_name, "pressed")
                            button_pressed = button_name
                            break

            if button_pressed is not None:
                if button_pressed == 'pre':
                    cpinx = (cpinx-1) if (cpinx>0) else (len(chrs)-1)
                if button_pressed == 'next':
                    cpinx = (cpinx+1) if (cpinx<len(chrs)-1) else 0
                if button_pressed == 'start':
                    run_mode = 1
                if button_pressed == 'answer':
                    run_mode = 2
            
            chessp.load_board(chrs[cpinx]['data'])
            cptext = font.render(chrs[cpinx]['name'], True, (255, 255, 255))

            # 绘制背景
            screen.blit(background, (0, 0))
            # 更新棋局
            chessp.draw()
            # 绘制blender
            screen.blit(blender, (BLD_x, BLD_y))
            # 绘制按钮
            for button in buttons.values():
                button.draw(screen)
            # 显示棋局名称
            w, h = cptext.get_size()
            screen.blit(cptext, (BLD_x+200-w/2, BLD_y))
            # 刷新窗口
            clock.tick(40)
            pygame.display.update()

        # 用户选择开始走棋, run_mode==1
        if run_mode == 1:
            # 记录时间和步数
            mins, secs = (0, 0)
            steps = 0
            # 记录鼠标拖动的标志和角色
            is_press = False
            elet_pressed = None
            # 记录历史步骤
            pre_steps = []
            # 走棋阶段
            while not chessp.is_finished():
                button_pressed = None
                # 捕获事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    elif event.type == ONESECOND:
                        secs += 1
                        mins, secs = (mins+1, 0) if secs>=60 else (mins, secs)
                        mins, secs = (0, 0) if mins>=60 else (mins, secs)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = event.pos
                            for e in chessp.elets:
                                if e.is_over(pos):
                                    is_press = True
                                    elet_pressed = e
                                    break

                            # 判断是否有控制按钮被按下
                            for button_name, button in playbtns.iteritems():
                                if button.is_over(event.pos):
                                    print (button_name, "pressed")
                                    button_pressed = button_name
                                    break

                    elif event.type == pygame.MOUSEMOTION:
                        if event.buttons[0] and is_press:
                            rel = event.rel
                            dest = None
                            if abs(rel[0])>abs(rel[1]) and (abs(rel[0]) > 3):
                                dest = 'right' if rel[0]>0 else 'left'
                            elif abs(rel[0])<abs(rel[1]) and (abs(rel[1]) > 3):
                                dest = 'down' if rel[1]>0 else 'up'
                            
                            if (dest!=None) and elet_pressed.can_move(dest):
                                dong.play()
                                elet_pressed.move_once(dest)
                                pre_steps.append((elet_pressed, dest))
                                steps += 1
                                chessp.display()
                                is_press = False
                                elet_pressed = None

                # 响应控制按钮响应
                if button_pressed == 'reset':
                    chessp.load_board(chrs[cpinx]['data'])
                    pre_steps = []
                    mins, secs = (0, 0)
                    steps = 0
                if button_pressed == 'home':
                    break
                if button_pressed == 'undo':
                    if len(pre_steps) > 0:
                        print('len(pre_steps)=', len(pre_steps))
                        e, d = pre_steps.pop()
                        e.move_once(redest_dic[d])
                        steps -= 1

                # 绘制背景
                screen.blit(background, (0, 0))
                # 更新棋局
                chessp.draw()
                # 绘制控制按钮
                for button in playbtns.values():
                    button.draw(screen)
                # 更新时间和步数
                tcost = sfont.render(u' %02d:%02d' % (mins, secs), True, (255, 255, 255))
                tstep = sfont.render(u'%d steps' % steps, True, (255, 255, 255))
                screen.blit(tcost, TIME_POS)
                cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                screen.blit(tstep, cpos)
                # 刷新窗口
                clock.tick(40)
                pygame.display.update()
            
            # 过关庆祝阶段
            if chessp.is_finished():
                wa.play()
                finish_cherr = False
                while not finish_cherr:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                        if event.type == MOUSEBUTTONDOWN:
                            finish_cherr = True

                    # 绘制背景
                    screen.blit(background, (0, 0))
                    # 显示棋局
                    chessp.draw()
                    # 显示时间和步数
                    screen.blit(tcost, TIME_POS)
                    cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                    screen.blit(tstep, cpos)
                    # 显示庆祝画面
                    screen.blit(cherrs, (BLD_x, BLD_y))
                    # 更新并显示爱心
                    group.update()
                    group.draw(screen)
                    # 刷新窗口
                    clock.tick(40)
                    pygame.display.update()
                cpinx = (cpinx+1) if (cpinx<len(chrs)-1) else 0
            
            # 复位记录变量
            run_mode = 0

        # 解密模式, run_mode==2
        if run_mode == 2:
            # 绘制背景
            screen.blit(background, (0, 0))
            # 显示棋局
            chessp.draw()
            # 显示blender
            screen.blit(blender, (BLD_x, BLD_y))
            # 显示信息提醒用户等待，解密需要最多8秒时间
            tips = font.render(u'calculating..', True, (255, 255, 255))
            tpos = (TIPS_POS[0]-tips.get_width()/2, TIPS_POS[1]-tips.get_height()/2)
            screen.blit(tips, tpos)
            pygame.display.update()
            # 解密
            answer = ksolute(chessp.get_data())
            
            # 演示过程
            pygame.time.set_timer(TWOSECOND, 1300)
            curix = 0 
            while True:
                button_pressed = None
                # 捕获事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    elif event.type == TWOSECOND:
                        if answerbtns['play'].get_status():
                            if curix < len(answer) - 1:
                                curix += 1
                                dong.play()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = event.pos
                            # 判断是否有控制按钮被按下
                            for button_name, button in answerbtns.iteritems():
                                if button.is_over(event.pos):
                                    print (button_name, "pressed")
                                    button_pressed = button_name
                                    break

                # 响应控制按钮响应
                if button_pressed == 'play':
                    answerbtns['play'].reverse()
                if button_pressed == 'home':
                    break
                if button_pressed == 'undo':
                    curix = (curix-1) if (curix>0) else curix

                # 绘制背景
                screen.blit(background, (0, 0))
                # 更新棋局
                chessp.load_board(answer[curix])
                chessp.draw()
                # 绘制控制按钮
                for button in answerbtns.values():
                    button.draw(screen)
                # 更新步数
                tstep = sfont.render(u'%d steps' % curix, True, (255, 255, 255))
                cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                screen.blit(tstep, cpos)
                # 刷新窗口
                clock.tick(40)
                pygame.display.update()
            pygame.time.set_timer(TWOSECOND, 0)

if __name__ == '__main__':
    main()

