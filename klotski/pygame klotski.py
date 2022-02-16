#coding=gbk

import copy
import pygame
import random
from pygame.locals import *
#from gameobjects.vector2 import *
from sys import exit
from datas import chrs
from ksolution import ksolute

# paths
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

K = 7       # 2x2 block king
H = 2       # 2x1 block
V = 3       # 1x2 block
P = 4       # 1x1 block
B = 0       # Blank
S = 1       # positions taken by extra block

# The size of the board
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

# Inverse direction definition
redest_dic = {
        'up' : 'down',
        'down' : 'up',
        'left' : 'right',
        'right' : 'left',
        }

# Characters paired with pictures
t2img_dict = {
        K:kingimg, H:hleaderimg,
        V:vleaderimg, P:pawnimg
        }

# Blocks
class Elet(object):

    # Different sizes of blocks
    tsize = { K:(2, 2), H:(2, 1), V:(1, 2), P:(1, 1)}

    # Initialize
    # target : paired surface
    # type ：type of block
    # loct : The logic position，The whole board is a 5x4 matrix, for example (0,2) is the first row, third column
    # kboard ：The datas for current board (a 2d array)
    def __init__(self, target, type, loct, kboard):
        self.surface = target
        self.type = type
        self.kboard = kboard
        self.loct = loct
        self.image = pygame.image.load(t2img_dict[type]).convert_alpha()

    # Make it in order for print
    def __str__(self):
        dic = {2:'H', 3:'V', 4:'P', 7:'K', 1:'S', 0:'B'}
        return 'type:%s loct:(%d, %d)' % (dic[self.type], self.loct[0], self.loct[1])

    # Draw blocks
    def draw(self):
        x, y = self.loct[1] * WID + LM, self.loct[0] * HID + TM
        self.surface.blit(self.image, (x, y))

    # Check if the blocks are in position
    def is_over(self, pos, WID=100, HID=100):
        x, y = self.loct[1] * WID + LM, self.loct[0] * HID + TM
        w, h = self.tsize[self.type][0]*WID, self.tsize[self.type][1]*HID
        return (x <= pos[0] < x + w) and (y <= pos[1] < y + h)

    # Move the block
    # dest : Direction，including 'up', 'left', 'right', 'down'
    def move_once(self, dest):
        # Check if the block is able to move, if not, return
        if not self.can_move(dest):
            return

        # Move the block
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

    # Check which direction a block could move
    # dest : direction 'up', 'left', 'right', 'down'
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

# Board
class Aspect():

    def __init__(self, target):
        self.surface = target
        self.kboard = None
        self.elets = []

    # Evaluate a board from a 2D array
    def load_board(self, pdata):
        self.clear()
        self.kboard = copy.deepcopy(pdata)
        for r in range(5):
            for c in range(4):
                if pdata[r][c] in (K, V, H, P):
                    e = Elet(self.surface, pdata[r][c], [r,c], self.kboard)
                    self.elets.append(e)

    # Draw elements
    def draw(self):
        for e in self.elets:
            e.draw()

    # Print
    def display(self):
        dic = {2:'H', 3:'V', 4:'P', 7:'K', 1:'S', 0:'B'}
        for r in self.kboard:
            rs = [dic[i] for i in r]
            print(' '.join(rs))
        print('')

    # End of check
    def is_finished(self):
        for e in self.elets:
            if (e.type == K) and (e.loct == [3, 1]):
                return True
        return False

    # Return data
    def get_data(self):
        return self.kboard

    # Clear
    def clear(self):
        self.kboard = None
        self.elets = []

# Buttoms
class Button(object):
    def __init__(self, image_filename, position):
        self.pos = position
        self.image = pygame.image.load(image_filename)

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    # Check if the point is in range
    def is_over(self, pos):
        pos_x, pos_y = pos
        x, y = self.pos
        w, h = self.image.get_size()
        return (x < pos_x <= x+w) and (y < pos_y <= y+h)



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

    pygame.init()

    clock  = pygame.time.Clock()

    screen = pygame.display.set_mode((420, 563), 0)

    # Load and transfer background
    background = pygame.image.load(bgimg).convert_alpha()
    blender = pygame.image.load(blenderimg).convert_alpha()
    cherrs = pygame.image.load(cherrsimg).convert_alpha()
    logo = pygame.image.load(logoimg)

    pygame.display.set_caption(u"Klotski")

    pygame.display.set_icon(logo)

    # clock event
    ONESECOND = USEREVENT + 1
    pygame.time.set_timer(ONESECOND, 1000)
    TWOSECOND = USEREVENT + 2
    pygame.time.set_timer(TWOSECOND, 0)

    font = pygame.font.Font("./res/msyh.ttf", 35)
    sfont = pygame.font.Font("./res/msyh.ttf", 24)


    chessp = Aspect(screen)

    # array
    cpinx = 0

    # Buttoms
    buttons = {}
    buttons['pre'] = Button(prebtnimg, (BLD_x, BLD_y))
    buttons['next'] = Button(nextbtnimg, (BLD_x+320, BLD_y))
    buttons['start'] = Button(startbtnimg, (BLD_x, BLD_y+60))
    buttons['answer'] = Button(answerbtnimg, (BLD_x+200, BLD_y+60))


    playbtns = {}
    playbtns['reset'] = Button(resetimg, RESET_POS)
    playbtns['home'] = Button(homeimg, HOME_POS)
    playbtns['undo'] = Button(undoimg, UNDO_POS)


    answerbtns = {}
    answerbtns['play'] = PlayPauseButton(pauseimg, playimg, RESET_POS)
    answerbtns['home'] = Button(homeimg, HOME_POS)
    answerbtns['undo'] = Button(undoimg, UNDO_POS)

    # Start loop
    while True:
        # Mode: 0:choose starting positions 1:play 2:solution
        run_mode = 0


        while run_mode == 0:
            button_pressed = None

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    # check which buttom is pressed
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

            # Draw background
            screen.blit(background, (0, 0))
            chessp.draw()
            # Draw blender
            screen.blit(blender, (BLD_x, BLD_y))
            for button in buttons.values():
                button.draw(screen)
            # Show the name of starting position
            w, h = cptext.get_size()
            screen.blit(cptext, (BLD_x+200-w/2, BLD_y))
            # Refresh
            clock.tick(40)
            pygame.display.update()

           # run_mode==1
        if run_mode == 1:
            # record the time and number of steps
            mins, secs = (0, 0)
            steps = 0
            # play the move
            is_press = False
            elet_pressed = None
            # record the steps
            pre_steps = []

            while not chessp.is_finished():
                button_pressed = None
                # event
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

                # buttom response
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

                # background
                screen.blit(background, (0, 0))
                chessp.draw()
                # control buttom
                for button in playbtns.values():
                    button.draw(screen)
                # refresh time and nof steps
                tcost = sfont.render(u' %02d:%02d' % (mins, secs), True, (255, 255, 255))
                tstep = sfont.render(u'%d steps' % steps, True, (255, 255, 255))
                screen.blit(tcost, TIME_POS)
                cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                screen.blit(tstep, cpos)
                clock.tick(40)
                pygame.display.update()

            # check if finished
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

                    # draw background
                    screen.blit(background, (0, 0))
                    chessp.draw()
                    # show time and nof steps
                    screen.blit(tcost, TIME_POS)
                    cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                    screen.blit(tstep, cpos)
                    clock.tick(40)
                    pygame.display.update()
                cpinx = (cpinx+1) if (cpinx<len(chrs)-1) else 0

            # reset the record
            run_mode = 0

        # run_mode==2
        if run_mode == 2:
            screen.blit(background, (0, 0))
            chessp.draw()
            screen.blit(blender, (BLD_x, BLD_y))
            answer = ksolute(chessp.get_data())

            # Show steps
            pygame.time.set_timer(TWOSECOND, 1300)
            curix = 0
            while True:
                button_pressed = None
                # Event
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
                            # Check bottoms
                            for button_name, button in answerbtns.iteritems():
                                if button.is_over(event.pos):
                                    print (button_name, "pressed")
                                    button_pressed = button_name
                                    break

                if button_pressed == 'play':
                    answerbtns['play'].reverse()
                if button_pressed == 'home':
                    break
                if button_pressed == 'undo':
                    curix = (curix-1) if (curix>0) else curix


                screen.blit(background, (0, 0))

                chessp.load_board(answer[curix])
                chessp.draw()
                for button in answerbtns.values():
                    button.draw(screen)
                # refresh steps
                tstep = sfont.render(u'%d steps' % curix, True, (255, 255, 255))
                cpos = (STEP_POS[0]-tstep.get_width()/2, STEP_POS[1])
                screen.blit(tstep, cpos)
                clock.tick(40)
                pygame.display.update()
            pygame.time.set_timer(TWOSECOND, 0)

if __name__ == '__main__':
    main()

