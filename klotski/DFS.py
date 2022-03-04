#coding=utf-8


import time
import numpy as np



King = 0
Soilder = 1
General2x1 = 2
General1x2 = 3
NU = 8
Blank = 9

board_1 = [[General2x1, King, NU, General2x1],
            [NU, NU, NU, NU],
            [General2x1, General1x2, NU, General2x1],
            [NU, Soilder, Soilder, NU],
            [Soilder, Blank, Blank, Soilder]]

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

    if chess == General1x2:
        if (row>0) and (move[row-1, column:column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row-1:row+1, column:column+2] = [[General1x2, NU], [Blank, Blank]]
            result.append(next)
        if (row<4) and (move[row+1, column:column+2]==[Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column:column+2] = [[Blank, Blank], [General1x2, NU]]
            result.append(next)
        if (column>0) and (move[row, column-1] == Blank).all():
            next = move.copy()
            next[row, column-1:column+2] = [General1x2, NU, Blank]
            result.append(next)
        if (column<2) and (move[row, column+2] == Blank).all():
            next = move.copy()
            next[row, column:column+3] = [Blank, General1x2, NU]
            result.append(next)

    if chess == General2x1 :
        if (row>0) and (move[row-1, column] == Blank).all():
            next = move.copy()
            next[row-1:row+2, column] = [General2x1 , NU, Blank]
            result.append(next)
        if (row<3) and (move[row+2, column] == Blank).all():
            next = move.copy()
            next[row:row+3, column] = [Blank, General2x1 , NU]
            result.append(next)
        if (column>0) and (move[row:row+2, column-1] == [Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column-1:column+1] = [[General2x1 , Blank], [NU, Blank]]
            result.append(next)
        if (column<3) and (move[row:row+2, column+1] == [Blank, Blank]).all():
            next = move.copy()
            next[row:row+2, column:column+2] = [[Blank, General2x1 ], [Blank, NU]]
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
            if nextmove[row, column] in (King, General1x2, General2x1, Soilder):
                Solve = mainloop(nextmove, row, column)
                possibles = [i.tolist() for i in Solve]
                result.extend(possibles)
    return result


# Return a list, each elements in steps represents each step
def DFS(board):
    # Storage in 1d array
    Moves = [board]


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
                break

        if EndDFS != -1:
            break

        # If not finish
        Continuemove = indexposition[-2] if (len(indexposition) >= 2) else indexposition[-1]
        endmove = len(Moves)
        for j in range(indexposition[-1], endmove):
            Possibles = Possibilities(Moves[j])
            # Filtering any already existed possible steps
            for k in Possibles:
                if k in Moves[Continuemove:]:
                    continue
                itemposition.append(j)
                Moves.append(k)

        indexposition.append(endmove)
        steps += 1

    # record the whole process
    result = [Moves[EndDFS]]
    while EndDFS != 0:
        EndDFS = itemposition[EndDFS]
        result.insert(0, Moves[EndDFS])

    return result



starttime = time.time()
result = DFS(board_1)
endtime = time.time()
print('Time cost for this solution: ', endtime - starttime)
print('Number of steps: ', len(result))