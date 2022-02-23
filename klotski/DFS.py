#coding=utf-8

import os
import time
import numpy as np
import datas
import dict



K = 7       # 2x2 block king
H = 2       # 2x1 block
V = 3       # 1x2 block
P = 4       # 1x1 block
B = 0       # Blank
S = 1       # positions taken by extra block

board_1 = [
    {

           [[P, K, S, P],
            [V, S, S, V],
            [S, H, S, S],
            [H, S, H, S],
            [B, P, P, B]] }],

# size of board
ROW = 5
COL = 4

# board element paired
dictionary = {0:'B', 1:'S', 2:'H', 3:'V', 4:'P', 7:'K'}


# print board
def kdisplay(board_1):
    print(board_1)

# give a position, return any possible moves after
# If the block cannot move, return empty
def mainloop(klotd, r, c):
    ret = []
    elet = klotd[r, c]

    if elet == K:
        if (r>0) and (klotd[r-1, c:c+2]==[B, B]).all():
            kcpy = klotd.copy()
            kcpy[r-1:r+2, c:c+2] = [[K, S], [S, S], [B, B]]
            ret.append(kcpy)
        if (r<3) and (klotd[r+2, c:c+2]==[B, B]).all():
            kcpy = klotd.copy()
            kcpy[r:r+3, c:c+2] = [[B, B], [K, S], [S, S]]
            ret.append(kcpy)
        if (c>0) and (klotd[r:r+2, c-1]==[B, B]).all():
            kcpy = klotd.copy()
            kcpy[r:r+2, c-1:c+2] = [[K, S, B], [S, S, B]]
            ret.append(kcpy)
        if (c<2) and (klotd[r:r+2, c+2]==[B, B]).all():
            kcpy = klotd.copy()
            kcpy[r:r+2, c:c+3] = [[B, K, S], [B, S, S]]
            ret.append(kcpy)

    if elet == H:
        if (r>0) and (klotd[r-1, c:c+2]==[B, B]).all():
            kcpy = klotd.copy()
            kcpy[r-1:r+1, c:c+2] = [[H, S], [B, B]]
            ret.append(kcpy)
        if (r<4) and (klotd[r+1, c:c+2]==[B, B]).all():
            kcpy = klotd.copy()
            kcpy[r:r+2, c:c+2] = [[B, B], [H, S]]
            ret.append(kcpy)
        if (c>0) and (klotd[r, c-1] == B).all():
            kcpy = klotd.copy()
            kcpy[r, c-1:c+2] = [H, S, B]
            ret.append(kcpy)
        if (c<2) and (klotd[r, c+2] == B).all():
            kcpy = klotd.copy()
            kcpy[r, c:c+3] = [B, H, S]
            ret.append(kcpy)

    if elet == V:
        if (r>0) and (klotd[r-1, c] == B).all():
            kcpy = klotd.copy()
            kcpy[r-1:r+2, c] = [V, S, B]
            ret.append(kcpy)
        if (r<3) and (klotd[r+2, c] == B).all():
            kcpy = klotd.copy()
            kcpy[r:r+3, c] = [B, V, S]
            ret.append(kcpy)
        if (c>0) and (klotd[r:r+2, c-1] == [B, B]).all():
            kcpy = klotd.copy()
            kcpy[r:r+2, c-1:c+1] = [[V, B], [S, B]]
            ret.append(kcpy)
        if (c<3) and (klotd[r:r+2, c+1] == [B, B]).all():
            kcpy = klotd.copy()
            kcpy[r:r+2, c:c+2] = [[B, V], [B, S]]
            ret.append(kcpy)

    if elet == P:
        if (r>0) and (klotd[r-1, c] == B):
            kcpy = klotd.copy()
            kcpy[r-1:r+1, c] = [P, B]
            ret.append(kcpy)
        if (r<4) and (klotd[r+1, c] == B):
            kcpy = klotd.copy()
            kcpy[r:r+2, c] = [B, P]
            ret.append(kcpy)
        if (c>0) and (klotd[r, c-1] == B):
            kcpy = klotd.copy()
            kcpy[r, c-1:c+1] = [P, B]
            ret.append(kcpy)
        if (c<3) and (klotd[r, c+1] == B):
            kcpy = klotd.copy()
            kcpy[r, c:c+2] = [B, P]
            ret.append(kcpy)

    return ret


# For a given board, return any possibilities of next step
def kchilds(klotd):
    ret = []
    cuk = np.asarray(klotd)
    # search for every blocks
    for r in range(ROW):
        for c in range(COL):
            if cuk[r, c] in (K, H, V, P):
                tcd = mainloop(cuk, r, c)
                childs = [i.tolist() for i in tcd]
                ret.extend(childs)
    return ret


# Return a list, each elements in steps represents each step
def ksolute(klotd):

    # Storage in 1d array
    kdbs = [klotd]
    # order the list, prodece an index
    prts = [-1]
    idxs = [0]

    # start DFS
    finish = -1
    steps = 0
    t1 = t2 = t3 = 0
    while True:
        
        # For loop to check any possibility
        for i in xrange(idxs[-1], len(kdbs)):
            if kdbs[i][3][1] == K:
                finish = i
                break

        if finish != -1:
            break

        # If not finish
        slip = idxs[-2] if (len(idxs)>=2) else idxs[-1]
        child = []
        endi = len(kdbs)
        for i in xrange(idxs[-1], endi):
            child = kchilds(kdbs[i])
            # Filtering any already existed possible steps
            for k in child:
                if k in kdbs[slip:]:
                    continue
                prts.append(i)
                kdbs.append(k)

        idxs.append(endi)
        steps += 1

    # record the whole process
    ret = [kdbs[finish]]
    while finish != 0:
        finish = prts[finish]
        ret.insert(0, kdbs[finish])

    return ret

# test
if __name__ == '__main__':
    data = [[B, B, B, B],
            [B, K, S, B],
            [B, S, S, B],
            [B, B, B, B],
            [B, B, B, B]]
    
    src = board_1
    kdisplay(src)
    time_start = time.time()
    ret = ksolute(src)
    time_end = time.time()
    print('Totally cast: %f s, %d steps', time_end - time_start, len(ret))


