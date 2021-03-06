import numpy as np
from time import perf_counter
import itertools
from tabulate import tabulate

board = np.array([
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1],
	[-1,-1, 1, 1, 1,-1,-1],
	[-1,-1, 1, 1, 1,-1,-1]
	])

# List of directions lists, representing all 24! possible orderings.
directions_tuples = list(itertools.permutations([(0, 2), (2, 0), (0, -2), (-2, 0)]))
directions_list = [list(element) for element in directions_tuples]

def find_solution(board, data = None):
	nodes_visited = []

	for i in range(24):
		rows = np.shape(board)[0] - 1
		columns = np.shape(board)[1] - 1

		def calculate_moves(board, x, y):
			x_old = x
			y_old = y
			possible_moves = []

			# Below are the direction vectors of all possible move directions in a given position (N,E,S,W).
			for direction in directions_list[i]:
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
				return True
			else:
				return False

		def board_code(board):
			""" Creates hash code for each board state which is unique up to rotational translation of board."""
			return hash(tuple(map(tuple, board)))

		visited = {board_code(board)}
		stats = {"End states:": 0, "Nodes visited:": 0, "Copies bypassed:": 0}
		
		def dfs(board, solution = []):
			""" Function uses DFS algorithm to find solution. """
			# Check if board is in goal state
			if is_solution(board):
				stats["End states:"] += 1
				stats["Nodes visited:"] = len(visited)
				nodes_visited.append(len(visited))
				return True

			possible_moves = generate_moves(board)
			if len(possible_moves) == 0:
				stats["End states:"] += 1

			# Generate the child nodes.
			child_nodes = []
			for move in possible_moves:
				child_nodes.append((move, update_board(np.copy(board), move)))
			
			for (move, child) in child_nodes:
				hash_code = board_code(child)
				if hash_code in visited:
					stats["Copies bypassed:"] += 1

				if hash_code not in visited:
					visited.add(hash_code)
					p = dfs(child, solution + [move])
					if p:
						return p

		run = dfs(board)
		if run:
			run
			if data:
				for data in stats:
					print(str(data), stats[data])
				print("="*65)
		else:
			print("\nNo solutions found!")
			print("="*65)
		
	return nodes_visited

def get_compass(lst):
	""" Converts list of cartesian direction vectors into cardinal directions. """
	for element in lst:
		if element == (0, 2):
			lst[lst.index((0, 2))] = 'N'
		elif element == (0,-2):
			lst[lst.index((0,-2))] = 'S'
		elif element == (2, 0):
			lst[lst.index((2, 0))] = 'E'
		else:
			lst[lst.index((-2,0))] = 'W'
	return''.join(lst)

nodes = find_solution(board)
compass_list = [get_compass(lst) for lst in directions_list]
results = tuple(zip(compass_list, nodes))        
col_names = ["Order", "Nodes visited"]
print("\n", tabulate(results, headers=col_names), "\n")


