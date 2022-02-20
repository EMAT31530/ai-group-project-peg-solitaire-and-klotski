#coding=utf-8
import numpy as np


# positioning

#                    S S
K = 7       # 2x2 block king
H = 2       # 2x1 block
V = 3       # 1x2 block
P = 4       # 1x1 block
B = 0       # Blank
S = 1       # positions taken by extra block

dictionary = {0:'B', 1:'S', 2:'H', 3:'V', 4:'P', 7:'K'}
# common starting positions
board_1 = [
    {
        'name':u'1. ',
        'data':
           [[P, K, S, P],
            [V, S, S, V],
            [S, H, S, S],
            [H, S, H, S],
            [B, P, P, B]] }],

print(board_1)
print("Input the matrix number u want to move ")
Movingblock=input()
self=dictionary(Movingblock) #the block in this position

print("Input the direction of the move, 'up','down','left','right'")
dest=input()

while True




# Check which direction a block could move, based on their types
# dest : direction 'up', 'left', 'right', 'down'
def can_move(self, dest):
    if (dest == 'up') and (self.loct[0] > 0):
        if (self.type in (P, V)) and (self.kboard[self.loct[0] - 1][self.loct[1]] == B):
            return True
        if (self.type in (K, H)) and (self.kboard[self.loct[0] - 1][self.loct[1]] == B) and \
                (self.kboard[self.loct[0] - 1][self.loct[1] + 1] == B):
            return True

    if (dest == 'down') and (self.loct[0] + self.tsize[self.type][1] < 5):
        if (self.type in (P, V)) and (self.kboard[self.loct[0] + self.tsize[self.type][1]][self.loct[1]] == B):
            return True
        if (self.type in (K, H)) and (self.kboard[self.loct[0] + self.tsize[self.type][1]][self.loct[1]] == B) and \
                (self.kboard[self.loct[0] + self.tsize[self.type][1]][self.loct[1] + 1] == B):
            return True

    if (dest == 'left') and (self.loct[1] > 0):
        if (self.type in (P, H)) and (self.kboard[self.loct[0]][self.loct[1] - 1] == B):
            return True
        if (self.type in (K, V)) and (self.kboard[self.loct[0]][self.loct[1] - 1] == B) and \
                (self.kboard[self.loct[0] + 1][self.loct[1] - 1] == B):
            return True

    if (dest == 'right') and (self.loct[1] + self.tsize[self.type][0] < 4):
        if (self.type in (P, H)) and (self.kboard[self.loct[0]][self.loct[1] + self.tsize[self.type][0]] == B):
            return True
        if (self.type in (K, V)) and (self.kboard[self.loct[0]][self.loct[1] + self.tsize[self.type][0]] == B) and \
                (self.kboard[self.loct[0] + 1][self.loct[1] + self.tsize[self.type][0]] == B):
            return True

    return False

def move_once(self, dest):
    # Check if the block is able to move using functions, if not, return
    if not self.can_move(dest):
        return

    # Move the block
        if dest == 'up':
            self.kboard[self.loct[0] - 1][self.loct[1]:self.loct[1] + 2] = [K, S]
            self.kboard[self.loct[0]][self.loct[1]:self.loct[1] + 2] = [S, S]
            self.kboard[self.loct[0] + 1][self.loct[1]:self.loct[1] + 2] = [B, B]
            self.loct[0] -= 1
        if dest == 'down':
            self.kboard[self.loct[0] + 1][self.loct[1]:self.loct[1] + 2] = [K, S]
            self.kboard[self.loct[0] + 2][self.loct[1]:self.loct[1] + 2] = [S, S]
            self.kboard[self.loct[0]][self.loct[1]:self.loct[1] + 2] = [B, B]
            self.loct[0] += 1
        if dest == 'left':
            self.kboard[self.loct[0]][self.loct[1] - 1:self.loct[1] + 1] = [K, S]
            self.kboard[self.loct[0] + 1][self.loct[1] - 1:self.loct[1] + 1] = [S, S]
            self.kboard[self.loct[0]][self.loct[1] + 1] = B
            self.kboard[self.loct[0] + 1][self.loct[1] + 1] = B
            self.loct[1] -= 1
        if dest == 'right':
            self.kboard[self.loct[0]][self.loct[1] + 1:self.loct[1] + 3] = [K, S]
            self.kboard[self.loct[0] + 1][self.loct[1] + 1:self.loct[1] + 3] = [S, S]
            self.kboard[self.loct[0]][self.loct[1]] = B
            self.kboard[self.loct[0] + 1][self.loct[1]] = B
            self.loct[1] += 1


def end_condition(self):
        for e in self.elets:
            if (e.type == K) and (e.loct == [3, 1]):
                return True
            return False



