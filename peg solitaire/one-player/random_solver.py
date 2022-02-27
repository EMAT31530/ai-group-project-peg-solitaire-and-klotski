import numpy as np
from time import perf_counter
import random

board = np.array([
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1]
	])

rows = np.shape(board)[0] - 1
columns = np.shape(board)[1] - 1

def calculate_moves(board, x, y):
	x_old = x
	y_old = y
	possible_moves = []

	# Below are the direction vectors of all possible move directions in a given position.
	for direction in [(0, 2), (0, -2), (-2, 0), (2, 0)]:
		x_new = x_old + direction[0]
		y_new = y_old + direction[1]
		# Here we make sure that the generated coordinates within the bounds of the board.
		if (0 <= x_new <= rows) and (0 <= y_new <= columns):
			if board[x_new, y_new] == 0:
				# Make sure that the midpoint is equal to 1.
				if board[int((x_old + x_new)/2), int((y_old + y_new)/2)]:
					possible_moves.append((x_new, y_new))

	return possible_moves

def generate_moves(board):

	possible_moves = []
	for x, y_values in enumerate(board):
		for y, state in enumerate(y_values):
			if state == 1:
				moves = calculate_moves(board, x, y)
				for move in moves:
					if move != []:
						possible_moves.append(((x, y), move))

	return possible_moves

def update_board(board, move):
	""" move = ((x_old, y_old), (x_new, y_new)) """
	# Remove peg from old position
	board[move[0][0]][move[0][1]] = 0
	# Add removed peg in empty position
	board[move[1][0]][move[1][1]] = 1
	# Remove 'hopped over' peg
	board[int((move[0][0] + move[1][0])/2)][int((move[0][1] + move[1][1])/2)] = 0

	return board

def is_solution(board):
	""" Checks if board is desired solution. """
	count = 0
	for row in board:
		for element in row:
			if element == 1:
				count += 1
	if (count == 1) and (board[3, 3] == 1):
		print("\nFinal board:")
		print(board)
		return True
	else:
		return False

def board_code(board):
		""" Creates hash code for each board state which is unique up to rotational translation of board."""
		return hash(tuple(map(tuple, board)))

stats = {"boards": 0}

def random_solver(board):
	stats["boards"] += 1
	possible_moves = generate_moves(board)

	if len(possible_moves) == 0:
		return board_code(board)
	next_move = random.choice(possible_moves)
	next_board =  update_board(board, next_move)

	p = random_solver(next_board)
	if p:
		return p

for _ in range(10000):
	random_solver(np.copy(board))

print("Average moves:", stats["boards"] / 10000)



