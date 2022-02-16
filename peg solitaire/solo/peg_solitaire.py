import numpy as np

board_1 = np.array([
	[2,2,1,1,1,2,2],
	[2,2,1,1,1,2,2],
	[1,1,1,1,1,1,1],
	[1,1,1,0,1,1,1],
	[1,1,1,1,1,1,1],
	[2,2,1,1,1,2,2],
	[2,2,1,1,1,2,2],
	])

print(board_1)

def find_moves(board, y, x):
	moves = []
	vectors = [(2, 0), (-2, 0), (0, -2), (0, 2)]

	for (j,i) in vectors:
		y_new = y + j
		x_new = x + i

		if (0 <= y_new <= 6) and (0 <= x_new <= 6):
			if board[y_new][x_new] == 0:
				if board[(y + y_new) // 2][(x + x_new) // 2] == 1:
					moves.append((y_new, x_new))

	return moves


def possible_moves(board):
	possible_moves = []

	for y, x_coordinates in enumerate(board):
		for x, state in enumerate(x_coordinates):
			if state == 1:
				moves = find_moves(board, y, x)
				for k in moves:
					possible_moves.extend([((y, x), k)])

	return possible_moves

print(possible_moves(board_1))

def update_board(board, y_old, x_old, y_new, x_new):
	
	
	board[y_old][x_old] = 0
	board[y_new][x_new] = 1
	board[(y_old + y_new) // 2][(x_old + x_new) // 2] = 0

	return board

board_2 = update_board(board_1, 1, 3, 3, 3)

print(board_2)

print(possible_moves(board_2))
