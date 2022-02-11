#coding=gbk

import copy
import pygame
import random
from pygame.locals import *
#from gameobjects.vector2 import *
from sys import exit
from datas import chrs
from ksolution import ksolute

# ��Դ·��
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

# ������ݺ궨��
# ���ڶ���ɫ��ֻ�����ϽǸ���K��H��V������ռλ����S
# ��K�������б�ʾΪ��K S
#                    S S
K = 7       # king������е�'�ܲ�'
H = 2       # ����Ϊ2�ĺ���Ԫ�أ�����еĺ����
V = 3       # ����Ϊ2������Ԫ�أ�����е������
P = 4       # ����Ϊ1��Ԫ�أ�����е�С��
B = 0       # ���ȶ�Ϊ1�Ŀհ�λ��
S = 1       # �����ɫ��ռλ��

# ����ߡ��������ϱ�������Blenderλ��
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

# ��������
redest_dic = {
        'up' : 'down',
        'down' : 'up',
        'left' : 'right',
        'right' : 'left',
        }

# ��ɫ��ͼƬ��Ӧ��ϵ
t2img_dict = { 
        K:kingimg, H:hleaderimg,
        V:vleaderimg, P:pawnimg
        }

# ��ɫ��
class Elet(object):

    # ��ɫ�Ŀ�߸���
    tsize = { K:(2, 2), H:(2, 1), V:(1, 2), P:(1, 1)}
    
    # ��ʼ��
    # target : ��Ӧ��surface
    # type ����ɫ���ͣ�����2��3��4��7����������ĺ궨��
    # loct : �߼�λ�ã���������Ϊ5x4����loctΪ�������У���(0, 2)��ʾ��һ�е�����
    # kboard ����ǰ������ݣ�Ϊһ����ά���飬�����'������ݺ궨��'
    def __init__(self, target, type, loct, kboard):
        self.surface = target
        self.type = type
        self.kboard = kboard
        self.loct = loct
        self.image = pygame.image.load(t2img_dict[type]).convert_alpha()
    
    # ���л������ڴ�ӡ��ʾ
    def __str__(self):
        dic = {2:'H', 3:'V', 4:'P', 7:'K', 1:'S', 0:'B'}
        return 'type:%s loct:(%d, %d)' % (dic[self.type], self.loct[0], self.loct[1])

    # ��surface�ϻ��ƽ�ɫ
    def draw(self):
        x, y = self.loct[1] * WID + LM, self.loct[0] * HID + TM
        self.surface.blit(self.image, (x, y))

    # �ж�ĳ������Ƿ��ڽ�ɫ��Χ��
    def is_over(self, pos, WID=100, HID=100):
        x, y = self.loct[1] * WID + LM, self.loct[0] * HID + TM
        w, h = self.tsize[self.type][0]*WID, self.tsize[self.type][1]*HID
        return (x <= pos[0] < x + w) and (y <= pos[1] < y + h)

    # ����ɫ��ĳ�����ƶ�һ��
    # dest : ����ȡֵΪ'up', 'left', 'right', 'down'
    def move_once(self, dest):
        # ���ж��ܷ��ƶ��������򷵻�
        if not self.can_move(dest):
            return 

        # �ƶ���ɫ
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

    # �жϽ�ɫ�Ƿ�����ĳ�������ƶ�
    # dest : ����ȡֵΪ'up', 'left', 'right', 'down'
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

# �����
class Aspect():
    
    def __init__(self, target):
        self.surface = target
        self.kboard = None
        self.elets = []

    # ��һ����ά�����������
    def load_board(self, pdata):
        self.clear()
        self.kboard = copy.deepcopy(pdata)
        for r in range(5):
            for c in range(4):
                if pdata[r][c] in (K, V, H, P):
                    e = Elet(self.surface, pdata[r][c], [r,c], self.kboard)
                    self.elets.append(e)

    # �������Ԫ��
    def draw(self):
        for e in self.elets:
            e.draw()

    # ��ӡ���
    def display(self):
        dic = {2:'H', 3:'V', 4:'P', 7:'K', 1:'S', 0:'B'}
        for r in self.kboard:
            rs = [dic[i] for i in r]
            print(' '.join(rs))
        print('')

    # �жϽ���
    def is_finished(self):
        for e in self.elets:
            if (e.type == K) and (e.loct == [3, 1]):
                return True
        return False

    # �����������(������ɫԪ��)
    def get_data(self):
        return self.kboard

    # ������
    def clear(self):
        self.kboard = None
        self.elets = []

# ��ť��
class Button(object):
    def __init__(self, image_filename, position):
        self.pos = position
        self.image = pygame.image.load(image_filename)

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    # ���point������Χ�ڣ�����True
    def is_over(self, pos):
        pos_x, pos_y = pos
        x, y = self.pos
        w, h = self.image.get_size()
        return (x < pos_x <= x+w) and (y < pos_y <= y+h)

# ����/��ͣ��ť��
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

# һ��������, ����İ��ģ����ڹ�����ף
class lover(pygame.sprite.Sprite):
    def __init__(self, target, image):
        pygame.sprite.Sprite.__init__(self)
        self.surface = target
        self.image = pygame.image.load(image).convert_alpha()
        self.rect  = self.image.get_rect()
        self.x = random.randint(0,target.get_width())   #��ʼ�����ĺ�����
        self.y = random.randint(0,target.get_height())  #��ʼ������������
        self.vx= random.randint(-3,3)                   #��ʼ�������ٶ�
        self.vy= random.randint(1,3)                    #��ʼ�������ٶ�
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
    # ��ʼ����Ƶ����
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    # ��ʼ��pygame����
    pygame.init()

    # ������ʱ��
    clock  = pygame.time.Clock()

    # ��������
    screen = pygame.display.set_mode((420, 563), 0)

    # ���ز�ת������
    background = pygame.image.load(bgimg).convert_alpha()
    blender = pygame.image.load(blenderimg).convert_alpha()
    cherrs = pygame.image.load(cherrsimg).convert_alpha()
    logo = pygame.image.load(logoimg)

    # ���ñ���
    pygame.display.set_caption(u"Klotski")

    # ����ͼ��
    pygame.display.set_icon(logo)

    # ������ʱ���¼�
    ONESECOND = USEREVENT + 1
    pygame.time.set_timer(ONESECOND, 1000)
    TWOSECOND = USEREVENT + 2
    pygame.time.set_timer(TWOSECOND, 0)

    # ��������
    font = pygame.font.Font("./res/msyh.ttf", 35)
    sfont = pygame.font.Font("./res/msyh.ttf", 24)

    # ����һ��������
    group = pygame.sprite.Group()
    # ����ͼ���ļ��б�
    fimages = ['res/star1.png', 'res/star2.png', 'res/star3.png']
    # ����80�����ľ���
    for i in range(80):
        index = random.randint(0, 2)
        lstar = lover(screen, fimages[index])
        group.add(lstar)

    # �������
    chessp = Aspect(screen)

    # �������
    cpinx = 0

    # ���ѡ�����İ�ť
    buttons = {}
    buttons['pre'] = Button(prebtnimg, (BLD_x, BLD_y))
    buttons['next'] = Button(nextbtnimg, (BLD_x+320, BLD_y))
    buttons['start'] = Button(startbtnimg, (BLD_x, BLD_y+60))
    buttons['answer'] = Button(answerbtnimg, (BLD_x+200, BLD_y+60))

    # ��������еİ�ť
    playbtns = {}
    playbtns['reset'] = Button(resetimg, RESET_POS)
    playbtns['home'] = Button(homeimg, HOME_POS)
    playbtns['undo'] = Button(undoimg, UNDO_POS)

    # ���ܹ����еİ�ť
    answerbtns = {}
    answerbtns['play'] = PlayPauseButton(pauseimg, playimg, RESET_POS)
    answerbtns['home'] = Button(homeimg, HOME_POS)
    answerbtns['undo'] = Button(undoimg, UNDO_POS)

    # ��ʼѭ��
    while True:
        # ����ģʽ��0:ѡ����� 1:���� 2:����
        run_mode = 0

        # ���ѡ��׶Σ�ѡ�������Կ�ʼ�����
        while run_mode == 0:
            button_pressed = None

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    # �ж��ĸ���ť������
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

            # ���Ʊ���
            screen.blit(background, (0, 0))
            # �������
            chessp.draw()
            # ����blender
            screen.blit(blender, (BLD_x, BLD_y))
            # ���ư�ť
            for button in buttons.values():
                button.draw(screen)
            # ��ʾ�������
            w, h = cptext.get_size()
            screen.blit(cptext, (BLD_x+200-w/2, BLD_y))
            # ˢ�´���
            clock.tick(40)
            pygame.display.update()

        # �û�ѡ��ʼ����, run_mode==1
        if run_mode == 1:
            # ��¼ʱ��Ͳ���
            mins, secs = (0, 0)
            steps = 0
            # ��¼����϶��ı�־�ͽ�ɫ
            is_press = False
            elet_pressed = None
            # ��¼��ʷ����
            pre_steps = []
            # ����׶�
            while not chessp.is_finished():
                button_pressed = None
                # �����¼�
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

                            # �ж��Ƿ��п��ư�ť������
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

                # ��Ӧ���ư�ť��Ӧ
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

                # ���Ʊ���
                screen.blit(background, (0, 0))
                # �������
                chessp.draw()
                # ���ƿ��ư�ť
                for button in playbtns.values():
                    button.draw(screen)
                # ����ʱ��Ͳ���
                tcost = sfont.render(u' %02d:%02d' % (mins, secs), True, (255, 255, 255))
                tstep = sfont.render(u'%d steps' % steps, True, (255, 255, 255))
                screen.blit(tcost, TIME_POS)
                cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                screen.blit(tstep, cpos)
                # ˢ�´���
                clock.tick(40)
                pygame.display.update()
            
            # ������ף�׶�
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

                    # ���Ʊ���
                    screen.blit(background, (0, 0))
                    # ��ʾ���
                    chessp.draw()
                    # ��ʾʱ��Ͳ���
                    screen.blit(tcost, TIME_POS)
                    cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                    screen.blit(tstep, cpos)
                    # ��ʾ��ף����
                    screen.blit(cherrs, (BLD_x, BLD_y))
                    # ���²���ʾ����
                    group.update()
                    group.draw(screen)
                    # ˢ�´���
                    clock.tick(40)
                    pygame.display.update()
                cpinx = (cpinx+1) if (cpinx<len(chrs)-1) else 0
            
            # ��λ��¼����
            run_mode = 0

        # ����ģʽ, run_mode==2
        if run_mode == 2:
            # ���Ʊ���
            screen.blit(background, (0, 0))
            # ��ʾ���
            chessp.draw()
            # ��ʾblender
            screen.blit(blender, (BLD_x, BLD_y))
            # ��ʾ��Ϣ�����û��ȴ���������Ҫ���8��ʱ��
            tips = font.render(u'calculating..', True, (255, 255, 255))
            tpos = (TIPS_POS[0]-tips.get_width()/2, TIPS_POS[1]-tips.get_height()/2)
            screen.blit(tips, tpos)
            pygame.display.update()
            # ����
            answer = ksolute(chessp.get_data())
            
            # ��ʾ����
            pygame.time.set_timer(TWOSECOND, 1300)
            curix = 0 
            while True:
                button_pressed = None
                # �����¼�
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
                            # �ж��Ƿ��п��ư�ť������
                            for button_name, button in answerbtns.iteritems():
                                if button.is_over(event.pos):
                                    print (button_name, "pressed")
                                    button_pressed = button_name
                                    break

                # ��Ӧ���ư�ť��Ӧ
                if button_pressed == 'play':
                    answerbtns['play'].reverse()
                if button_pressed == 'home':
                    break
                if button_pressed == 'undo':
                    curix = (curix-1) if (curix>0) else curix

                # ���Ʊ���
                screen.blit(background, (0, 0))
                # �������
                chessp.load_board(answer[curix])
                chessp.draw()
                # ���ƿ��ư�ť
                for button in answerbtns.values():
                    button.draw(screen)
                # ���²���
                tstep = sfont.render(u'%d steps' % curix, True, (255, 255, 255))
                cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                screen.blit(tstep, cpos)
                # ˢ�´���
                clock.tick(40)
                pygame.display.update()
            pygame.time.set_timer(TWOSECOND, 0)

if __name__ == '__main__':
    main()

