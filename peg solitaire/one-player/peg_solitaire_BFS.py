import numpy as np

board = np.array([
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1]
	])

def calculate_moves(board, x, y):
	x_old = x
	y_old = y
	possible_moves = []
	# Below are the direction vectors of all possible move directions in a given position
	for direction in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
		x_new = x_old + direction[0]
		y_new = y_old + direction[1]
		# Here we make sure that the generated coordinates within the bounds of the board
		if (0 <= x_new <= 6) and (0 <= y_new <= 6):
			if board[x_new, y_new] == 0:
				# Make sure that the midpoint is equal to 1
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
	"""
	move = ((x_old, y_old), (x_new, y_new))
	"""
	# Remove peg from old position
	board[move[0][0]][move[0][1]] = 0
	# Add removed peg in empty position
	board[move[1][0]][move[1][1]] = 1
	# Remove 'hopped over' peg
	board[int((move[0][0] + move[1][0])/2)][int((move[0][1] + move[1][1])/2)] = 0

	return board

def evaluate_board(board):
	count = 0
	for row in board:
		for element in row:
			if element == 1:
				count += 1
	if (count == 1) and board[3, 3] == 1:
		print("Solution found!\n")
		print(board)
		return 0
	else:
		return count

def board_code(board):
	"""
	Function creates unique hash code for each board state.
	"""
	return hash(tuple(map(tuple, board)))

#######################################################################################################################

visited = set()
stats = {"count": 0}

def bfs(queue):
	nodes = []
	while queue:
		current_board = queue.pop(0)
		if evaluate_board(current_board) == 0:
			print("Solution found!")
			return 0
		possible_moves = generate_moves(current_board)
		child_nodes = []
		for move in possible_moves:
			child_nodes.append(update_board(np.copy(current_board), move))		
		for child in child_nodes:
			hash_code = board_code(child)
			if hash_code not in visited:
				visited.add(hash_code)
				nodes.append(child)
	stats["count"] += 1
	print("Nodes on level " + str(stats["count"]) + ":", len(nodes))
		
	p = bfs(nodes)
	output = bfs(p)
	if output != 0:
		return output

# Unfortunately the bfs process is too inefficient for this problem.
# DFS is much better suited to the problem.
# Below we terminate bfs if the runtime exceeds 20 seconds.

import multiprocessing
import time

if __name__ == '__main__':
	p = multiprocessing.Process(target=bfs, name="bfs", args=([board],))
	p.start()
	print("\nNodes on level 0: 1")
	time.sleep(20)
	print("\nTime limit exceeded! Process terminated!\nBFS incomplete!\n")
	p.terminate()
	p.join()
