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
dictionary = {0:'B', 1:'S', 2:'H', 3:'V', 4:'P', 7:'K'}

# print board
