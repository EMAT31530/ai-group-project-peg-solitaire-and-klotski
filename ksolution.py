#coding=utf-8

import os
import time
import numpy as np
from datas import chrs

K = 7       # 2x2 block king
H = 2       # 2x1 block
V = 3       # 1x2 block
P = 4       # 1x1 block
B = 0       # Blank
S = 1       # positions taken by extra block

# size of board
ROW = 5
COL = 4

# board element paired
kdic = {0:'B', 1:'S', 2:'H', 3:'V', 4:'P', 7:'K'}

# print board
def kdisplay(klotd):
    for r in range(ROW):
        td = klotd[r]
        print(' '.join([kdic[i] for i in td]))
    print('')

# give a position, return any possible moves after
# If the block cannot move, return empty
def knexts(klotd, r, c):
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


# 给定一个棋局，返回该棋局的所有下一步可能的棋局(子棋局)
def kchilds(klotd):
    ret = []
    cuk = np.asarray(klotd)
    # search for every blocks
    for r in range(ROW):
        for c in range(COL):
            if cuk[r, c] in (K, H, V, P):
                tcd = knexts(cuk, r, c)
                childs = [i.tolist() for i in tcd]
                ret.extend(childs)
    return ret

# 给定一个棋局(仅数据部分，不要name)，返回解法
# 返回一个列表，从前往后每一个元素是一步对应的棋局
def ksolute(klotd):

    # 产生的棋局库, # 为了后续查找方便，使用一维列表存储，
    kdbs = [klotd]
    # 同时用一个列表来记录父子关系，用一个列表记录每一层的首元素索引
    prts = [-1]
    idxs = [0]

    # 开始穷举，过程中删除库或对称库中已有棋局
    finish = -1
    steps = 0
    t1 = t2 = t3 = 0
    while True:
        
        # 对当前层所有棋局进行判断, 有完成的则退出
        for i in xrange(idxs[-1], len(kdbs)):
            if kdbs[i][3][1] == K:
                finish = i
                break

        if finish != -1:
            break

        # 如果当前层没有已完成的棋局, 则生成下一层
        slip = idxs[-2] if (len(idxs)>=2) else idxs[-1]
        child = []
        endi = len(kdbs)
        for i in xrange(idxs[-1], endi):
            child = kchilds(kdbs[i])
            # 过滤生成子棋局, 若与棋局库中重复则删除, 否则入库
            # 只搜索最近2层, 因为如果再往前层里有过该局，那该局的父节点不会存在
            for k in child:
                if k in kdbs[slip:]:
                    continue
                prts.append(i)
                kdbs.append(k)

        idxs.append(endi)
        steps += 1

    # 回溯，找到完整的过程并记录
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
    
    src = chrs[1]['data']
    kdisplay(src)
    #src = np.asarray(data)
    time_start = time.time()
    ret = ksolute(src)
    time_end = time.time()
    print('Totally cast: %f s, %d steps', time_end - time_start, len(ret))
    #_ = raw_input('Please press anykey to display steps...')
    #ret = knexts(klot, 1, 1)
    #ret = kchilds(klot)
    #for k in ret:
    #    os.system('cls')
    #    kdisplay(k)
    #    time.sleep(1)

