import random
import time
import queue

dirr = [1, 0, -1, 0]
dirc = [0, 1, 0, -1]

class Piece:

    def __init__(self, name, row, col, height, width):
        self.name = name
        self.row = row
        self.col = col
        self.height = height
        self.width = width

    def copy(self):
        return Piece(self.name, self.row, self.col, self.height, self.width)

    def __str__(self):
        return self.name + " " + str(self.row) + ' ' + str(self.col) + ' '+ str(self.height) + ' ' + str(self.width)

class Board:

    def __init__(self):
        self.row_size = 5
        self.col_size = 4
        self.pieces = []
        self.reset_piece()

    def reset_piece(self):
        self.pieces.clear()

        self.pieces.append(Piece('卒', 0, 0, 1, 1))
        self.pieces.append(Piece('卒', 0, 3, 1, 1))
        self.pieces.append(Piece('卒', 3, 1, 1, 1))
        self.pieces.append(Piece('卒', 3, 2, 1, 1))
        self.pieces.append(Piece('曹', 1, 1, 2, 2))
        self.pieces.append(Piece('赵', 1, 0, 2, 1))
        self.pieces.append(Piece('关', 3, 0, 2, 1))
        self.pieces.append(Piece('黄', 1, 3, 2, 1))
        self.pieces.append(Piece('马', 3, 3, 2, 1))
        self.pieces.append(Piece('张', 0, 1, 1, 2))

    def print_board(self):
        board = []
        for i in range(self.row_size):
            x = ['空' for j in range(self.col_size)]
            board.append(x)
        for piece in self.pieces:
            for i in range(piece.height):
                for j in range(piece.width):
                    board[piece.row + i][piece.col + j] = piece.name
        for x in board:
            print(' '.join(x))

    def __str__(self):
        board = []
        for i in range(self.row_size):
            x = ['空' for j in range(self.col_size)]
            board.append(x)
        for piece in self.pieces:
            for i in range(piece.height):
                for j in range(piece.width):
                    board[piece.row + i][piece.col + j] = piece.name
        res = ''
        for x in board:
            res += ' '.join(x) + '\n'
        return res

    def copy(self):
        b = Board()
        b.pieces.clear()
        for piece in self.pieces:
            b.pieces.append(piece.copy())
        return b

    def valid(self):
        board = []
        for i in range(self.row_size):
            x = ['空' for j in range(self.col_size)]
            board.append(x)
        for piece in self.pieces:
            for i in range(piece.height):
                for j in range(piece.width):
                    if piece.row + i < 0 or piece.row + i >= self.row_size or piece.col + j < 0 or piece.col + j >= self.col_size:
                        return False
                    if board[piece.row + i][piece.col + j] != '空':
                        return False
                    board[piece.row + i][piece.col + j] = piece.name
        return True

    def move(self, piece, dir):
        b = self.copy()
        piece.row += dirr[dir]
        piece.col += dirc[dir]
        if not self.valid():
            self.pieces = b.pieces
            return False
        return True

    def find_by_piece(self, name):
        for piece in self.pieces:
            if piece.name == name:
                return piece
        return None

    def is_win(self):
        piece = self.find_by_piece('曹')
        return piece.row == 3 and piece.col == 1

    def all_moves(self):
        lst = []
        for i in range(len(self.pieces)):
            for dir in range(4):
                c = self.copy()
                if c.move(c.pieces[i], dir):
                    lst.append([i, dir])
        return lst

def print_steps(d, s):
    if s is None:
        return '', 0
    pres, steps = print_steps(d, d[s])
    return pres + '第%d步' % steps + '\n' + s + '\n', steps + 1


def simulate():
    d = {}
    b = Board()
    d[str(b)] = None
    while True:
        if b.is_win():
            return print_steps(d, str(b))
        ok = False
        for i in range(150):
            c = b.copy()
            all_moves = c.all_moves()
            index, dir = random.choice(all_moves)
            c.move(c.pieces[index], dir)
            if str(c) not in d:
                d[str(c)] = str(b)
                ok = True
                b = c
                break
        if not ok:
            return False

def one_run():
    while True:
        ret = simulate()
        if ret is not False:
            return ret

def more_runs():
    value, min_steps = '', 999999999
    runs = 15
    for i in range(runs):
        print('正在进行第%d次模拟' % (i + 1))
        res, steps = one_run()
        if min_steps > steps:
            min_steps = steps
            value = res
        print('模拟结果为耗费%d步，当前最短%d步' % (steps, min_steps))
    print(value)

if __name__ == '__main__':
    start = time.time()
    more_runs()
    end = time.time()
    print('本次计算时间: ', end - start)

