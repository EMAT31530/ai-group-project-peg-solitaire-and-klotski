import numpy as np
from time import perf_counter

board = np.array([
	[ 2, 2, 1, 1, 1, 2, 2],
	[ 2, 2, 1, 1, 1, 2, 2],
	[ 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[ 2, 2, 1, 1, 1, 2, 2],
	[ 2, 2, 1, 1, 1, 2, 2]
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
		print("\nSolution found!\n")
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

visited = {board_code(board)}
stats = {"End states found:": 1, "Nodes visited:": 0, "Copies bypassed:": 0}

def dfs(board, solution = ()):
	if evaluate_board(board) == 0:
		stats["Nodes visited:"] = len(visited)
		print("\nSolution length:", len(solution))
		print("Solution:")
		for x in solution:
			print(x[0], "->", x[1])
		return solution
	# These moves will generate the child nodes/boards
	possible_moves = generate_moves(board)
	if len(possible_moves) == 0:
		stats["End states found:"] += 1
	nodes = []
	for move in possible_moves:
		nodes.append(update_board(np.copy(board), move))
	for child in nodes:
		if board_code(child) in visited:
			stats["Copies bypassed:"] += 1
		hash_code = board_code(child)
		if hash_code not in visited:
			visited.add(hash_code)
			output = dfs(child, [x for x in solution]+[move])
			if output:
				return output

t = perf_counter()
print("\nStart board:\n")
print(board)
dfs(board)
print("\n")
for data in stats:
	print(str(data), stats[data])
print("runtime:", perf_counter() - t, "\n")
