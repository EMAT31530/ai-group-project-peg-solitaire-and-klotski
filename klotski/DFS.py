#coding=utf-8


import time
import numpy as np



King = 0
Soilder = 1
General1x2 = 2
General2x1 = 3
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


def board_code(board):
    """ Creates hash code for each board state which is unique up to rotational translation of board."""
    return hash(tuple(map(tuple, board)))


# Return a list, each elements in steps represents each step
def DFS(board):
    # Store in array
    Moves = [board]
    chessposition = [-1]
    indexposition = [0]
    EndDFS = -1
    steps = 0
    hashstorage = []

    while True:

        # For loop to check any possibility

        for j in range(indexposition[-1], len(Moves)):
            if Moves[j][3][1] == King:
                EndDFS = j
                break #Break if reaches end

        if EndDFS != -1:
            break


        Continuemove = indexposition[-2] if (len(indexposition) >= 2) else indexposition[-1]
        endmove = len(Moves)
        for j in range(indexposition[-1], endmove):


            print(hashstorage)
            # Filtering any already existed possible steps
            for k in hashstorage:
                if k in Moves[Continuemove]:
                    continue

                chessposition.append(j)
                Moves.append(k)
                hashstorage = hashstorage.append(board_code(Moves[j]))

        indexposition.append(endmove)
        steps += 1

    # record the whole process
    result = [Moves[EndDFS]]
    while EndDFS != 0:
        EndDFS = chessposition[EndDFS]
        result.insert(0, Moves[EndDFS])

    return result




starttime = time.time()
result = DFS(board_1)

print('Time cost for this solution: ', endtime - starttime)
print('Number of steps: ', len(result))

