import numpy as np
from time import perf_counter
import resource

# English board
board = np.array([
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1]
	])

def find_solution(board):
	print("\nStart board:")
	print(board)

	def calculate_moves(board, x, y):
		rows = np.shape(board)[0] - 1
		columns = np.shape(board)[1] - 1
		x_old = x
		y_old = y
		possible_moves = []

		# Below are the direction vectors of all possible move directions in a given position.
		for direction in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
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
		""" Finds all possible moves in a given board state. """
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
		if count == 1:
		# Include instead if considering specific end location to solution
		# if count == 1 and board[3, 3] == 1:
			print("\nSolution found!\n\nFinal board:")
			print(board)
			return True
		else:
			return False

	def board_code(board):
		""" Creates hash code for each board state which is unique up to rotational translation of board."""
		return hash(tuple(map(tuple, board)))

	visited = {board_code(board)}
	data = {"Nodes visited:": 0, "Nodes skipped:": 0, "End states:": 0}
	branch_factors = []
	
	def dfs(board):
		""" Function uses DFS algorithm to find solution. """
		# Check if board is in goal state
		if is_solution(board):
			data["Nodes visited:"] = len(visited)
			data["End states:"] += 1
			return True

		possible_moves = generate_moves(board)
		if len(possible_moves) == 0:
			data["End states:"] += 1

		# Generate the child nodes.
		child_nodes = []
		for move in possible_moves:
			child_nodes.append((move, update_board(np.copy(board), move)))
		
		for (move, child) in child_nodes:
			hash_code = board_code(child)
			if hash_code in visited:
				data["Nodes skipped:"] += 1

			if hash_code not in visited:
				visited.add(hash_code)
				p = dfs(child)
				if p:
					return p

	t = perf_counter()
	if dfs(board) == True:
		for stat in data:
			print(str(stat), data[stat])
		# print("Average branch factor:", round(sum(branch_factors) / len(branch_factors), 3))
	else:
		print("\nNo solutions found!")
	print("Runtime:", perf_counter() - t, "seconds")


find_solution(board)
r = resource.getrusage(resource.RUSAGE_SELF)
print(f'Memory usage (MB): {r.ru_maxrss / 1000000}')