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
	possible_moves = []
	moves = [(2, 0), (-2, 0), (0, -2), (0, 2)]

	for (j,i) in moves:
		y_new = y + j
		x_new = x + i

		if (0 <= y_new <= 6) and (0 <= x_new <= 6):
			if board[y_new][x_new] == 0:
				# we need ot find possible moves
	
	#return possible_moves

print(find_moves(board_1,3,3))

