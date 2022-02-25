#coding=utf-8


import time
import numpy as np



King = 0
Soilder = 1
General1x2 = 2
General2x1 = 3
NU = 8
Blank = 9


board_1 = [[Soilder, King, NU, Soilder],
            [General1x2, NU, NU, General1x2],
            [NU, General2x1, NU, NU],
            [General2x1, NU, General2x1, NU],
            [Blank, Soilder, Soilder, Blank]]

print(board_1)

# size of board
ROW = 5
COL = 4

# board element paired
dictionary = {9:'Blank', 8:'NU', 3:'General2x1', 2:'General1x2', 1:'Soilder', 0:'King'}


# give a position, return any possible moves after
# If the block cannot move, return empty
def mainloop(move, row, column):
    result = []
    chess = move[row, column]

    if chess == King:
        if (row>0) and (move[row-1, column:column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row-1:row+2, column:column+2] = [[King, NU], [NU, NU], [Blank, Blank]]
            result.append(next)
        if (row<3) and (move[row+2, column:column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row:row+3, column:column+2] = [[Blank, Blank], [King, NU], [NU, NU]]
            result.append(next)
        if (column>0) and (move[row:row+2, column-1]==[Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column-1:column+2] = [[King, NU, Blank], [NU, NU, Blank]]
            result.append(next)
        if (column<2) and (move[row:row+2, column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column:column+3] = [[Blank, King, NU], [Blank, NU, NU]]
            result.append(next)

    if chess == General2x1:
        if (row>0) and (move[row-1, column:column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row-1:row+1, column:column+2] = [[General2x1, NU], [Blank, Blank]]
            result.append(next)
        if (row<4) and (move[row+1, column:column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column:column+2] = [[Blank, Blank], [General2x1, NU]]
            result.append(next)
        if (column>0) and (move[row, column-1] == Blank).all():
            next = move.copy()
            next[row, column-1:column+2] = [General2x1, NU, Blank]
            result.append(next)
        if (column<2) and (move[row, column+2] == Blank).all():
            next = move.copy()
            next[row, column:column+3] = [Blank, General2x1, NU]
            result.append(next)

    if chess == General1x2 :
        if (row>0) and (move[row-1, column] == Blank).all():
            next = move.copy()
            next[row-1:row+2, column] = [General1x2, NU, Blank]
            result.append(next)
        if (row<3) and (move[row+2, column] == Blank).all():
            next = move.copy()
            next[row:row+3, column] = [Blank, General1x2, NU]
            result.append(next)
        if (column>0) and (move[row:row+2, column-1] == [Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column-1:column+1] = [[General1x2, Blank], [NU, Blank]]
            result.append(next)
        if (column<3) and (move[row:row+2, column+1] == [Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column:column+2] = [[Blank, General1x2], [Blank, NU]]
            result.append(next)

    if chess == Soilder:
        if (row>0) and (move[row-1, column] == Blank):
            next = move.copy()
            next[row-1:row+1, column] = [Soilder, Blank]
            result.append(next)
        if (row<4) and (move[row+1, column] == Blank):
            next = move.copy()
            next[row:row+2, column] = [Blank, Soilder]
            result.append(next)
        if (column>0) and (move[row, column-1] == Blank):
            next = move.copy()
            next[row, column-1:column+1] = [Soilder, Blank]
            result.append(next)
        if (column<3) and (move[row, column+1] == Blank):
            next = move.copy()
            next[row, column:column+2] = [Blank, Soilder]
            result.append(next)

    return result


# For a given board, return any possibilities of next step
def Possibilities(move):
    result = []
    nextmove = np.asarray(move)
    # search for every blocks
    for row in range(ROW):
        for column in range(COL):
            if nextmove[row, column] in (King, General2x1, General1x2, Soilder):
                Solve = mainloop(nextmove, row, column)
                possibles = [i.tolist() for i in Solve]
                result.extend(possibles)
    return result

def eff_key(self):
    grid = self.grid
    return " ".join([str(eff_block[grid[i][j]]) for i in range(5) for j in range(4)])

def BFS(source: State, dest: State):
    # Storage in 1d array
    Moves = [move]


    itemposition = [-1]
    indexposition = [0]

    # start DFS
    EndDFS = -1
    steps = 0

    while True:

        # For loop to check any possibility

        for j in range(indexposition[-1], len(Moves)):
            if Moves[j][3][1] == King:
                EndDFS = j
                break #Break if reaches end

        if EndDFS != -1:
            break

    vis = set()
    par = {b: None}
    q = [b]
    vis.add(b.eff_key())
    sol_found = False
    cur_board = None
    while len(q) > 0:
        cur_board = q[0]
        q = q[1:]
        next_boards = cur_board.all_boards(vis)
        for board in next_boards:
            if board.eff_key() not in vis:
                q.append(board)
                vis.add(board.eff_key())
                par[board] = cur_board
                if board.solved():
                    cur_board = board
                    sol_found = True
                    break
        if sol_found:
            break

    solution = []
    if sol_found:
        while cur_board != None:
            solution.append(cur_board)
            cur_board = par[cur_board]
        solution.reverse()
        for sol in solution:
            sol.print_grid()

starttime = time.time()
result = DFS(board_1)
endtime = time.time()
print('Time cost for this solution: ', endtime - starttime)
print('Number of steps: ', len(result))