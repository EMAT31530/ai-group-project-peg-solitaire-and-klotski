import random
import time
import queue

dirr = [1, 0, -1, 0]
dirc = [0, 1, 0, -1]

class chess:

    def __init__(self, name, row, col, height, width):
        self.name = name
        self.row = row
        self.col = col
        self.height = height
        self.width = width

    def copy(self): #For refresh board
        return chess(self.name, self.row, self.col, self.height, self.width)

    def __str__(self):
        return self.name + " " + str(self.row) + ' ' + str(self.col) + ' '+ str(self.height) + ' ' + str(self.width)

class Board:

    def __init__(self): #Board size
        self.row_size = 5
        self.col_size = 4
        self.chess = []
        self.reset_chess()

    def reset_chess(self): #Import initial conditions
        self.chess.clear()

        self.chess.append(chess('soilder', 0, 0, 1, 1))
        self.chess.append(chess('soilder', 0, 3, 1, 1))
        self.chess.append(chess('soilder', 3, 1, 1, 1))
        self.chess.append(chess('soilder', 3, 2, 1, 1))
        self.chess.append(chess('King', 1, 1, 2, 2))
        self.chess.append(chess('general2x1', 1, 0, 2, 1))
        self.chess.append(chess('general2x1', 3, 0, 2, 1))
        self.chess.append(chess('general2x1', 1, 3, 2, 1))
        self.chess.append(chess('general2x1', 3, 3, 2, 1))
        self.chess.append(chess('general1x2', 0, 1, 1, 2))

    def print_board(self):
        board = []
        for i in range(self.row_size): #consider the size of chess
            x = ['0' for j in range(self.col_size)]
            board.append(x)
        for chess in self.chess: #print chess with their given size
            for i in range(chess.height):
                for j in range(chess.width):
                    board[chess.row + i][chess.col + j] = chess.name
        for x in board:
            print(' '.join(x))

    def __str__(self):#when chess is moved, represent(their name in string) on board
        board = []
        for i in range(self.row_size):
            x = ['0' for j in range(self.col_size)]
            board.append(x)
        for chess in self.chess:
            for i in range(chess.height):
                for j in range(chess.width):
                    board[chess.row + i][chess.col + j] = chess.name
        res = ''
        for x in board:
            res += ' '.join(x) + '\n'
        return res

    def copy(self): #refresh board
        b = Board()
        b.chess.clear()
        for chess in self.chess:
            b.chess.append(chess.copy())
        return b

    def valid(self): #Check which chess, which direction is available
        board = []
        for i in range(self.row_size):
            x = ['0' for j in range(self.col_size)]
            board.append(x)
        for chess in self.chess:
            for i in range(chess.height):
                for j in range(chess.width):
                    if chess.row + i < 0 or chess.row + i >= self.row_size or chess.col + j < 0 or chess.col + j >= self.col_size:
                        return False
                    if board[chess.row + i][chess.col + j] != '0':
                        return False
                    board[chess.row + i][chess.col + j] = chess.name
        return True

    def move(self, chess, dir):
        b = self.copy()
        chess.row += dirr[dir]
        chess.col += dirc[dir]
        if not self.valid():
            self.chess = b.chess
            return False
        return True

    def find_by_chess(self, name): #used for win condition
        for chess in self.chess:
            if chess.name == name:
                return chess
        return None

    def is_win(self): #win condition
        chess = self.find_by_chess('King')
        return chess.row == 3 and chess.col == 1

    def all_moves(self):
        lst = []
        for i in range(len(self.chess)):
            for dir in range(4):
                c = self.copy() #copy the last move if it stays
                if c.move(c.chess[i], dir):
                    lst.append([i, dir])
        return lst

def print_steps(d, s):
    if s is None:
        return '', 0
    pres, steps = print_steps(d, d[s])
    return pres + 'Number of steps%d' % steps + '\n' + s + '\n', steps + 1


def simulate(): #Monte Carlo
    d = {} #storage
    b = Board()
    d[str(b)] = None
    while True:
        if b.is_win(): #end counting if win
            return print_steps(d, str(b))
        ok = False
        for i in range(5):  #defult policy
            c = b.copy()
            all_moves = c.all_moves()
            index, dir = random.choice(all_moves) #Random choice move
            c.move(c.chess[index], dir)
            if str(c) not in d: #Avoid states that have already been visited
                d[str(c)] = str(b)
                ok = True
                b = c
                break
        if not ok:
            return False

def stop(): #stop when one result is found
    while True:
        ret = simulate()
        if ret is not False:
            return ret

def more_runs():
    value, min_steps = '', 999999999 #Value to unpack
    runs = 15 #set interation number
    for i in range(runs):
        print('interation number %d' % (i + 1))
        res, steps = stop()
        if min_steps > steps: #Take the shortest solution
            min_steps = steps
            value = res
        print('steps for this interation is %d，shortest path for now is %d' % (steps, min_steps))
    print(value)

#Run the program, count time
start = time.time()
more_runs()
end = time.time()
print('Running time: ', end - start)
