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

rows = np.shape(board)[0] - 1
columns = np.shape(board)[1] - 1

def calculate_moves(board, x, y):
	x_old = x
	y_old = y
	possible_moves = []
	# Below are the direction vectors of all possible move directions in a given position
	# for direction in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
	for direction in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
		x_new = x_old + direction[0]
		y_new = y_old + direction[1]
		# Here we make sure that the generated coordinates within the bounds of the board
		if (0 <= x_new <= rows) and (0 <= y_new <= columns):
			if board[x_new, y_new] == 0:
				# Make sure that the midpoint is equal to 1
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
	count = 0
	for row in board:
		for element in row:
			if element == 1:
				count += 1
	if count == 1:
	# Include instead if considering specific end location to solution
	# if count == 1 and board[3,3] == 1:
		print("\nSolution found!")
		print("Final board:")
		print(board)
		return True
	else:
		return False

def board_code(board):
	""" Function creates unique hash code for each board state which is unique by rotation."""
	return hash(tuple(map(tuple, board)))

#####################################################################################################################

# Board dimensions
x_size = np.shape(board)[0]
y_size = np.shape(board)[1]

def peg_count(board):
	"""will act as heuristic too"""
	count = 0
	for x in range(x_size):
		for y in range(y_size):
			if board[x][y] == 1:
				count += 1
	return count

# Define middle of the board for heuristic 1
mid_x = int(x_size / 2)
mid_y = int(y_size / 2)

def h1(board):
	""" furthest peg from centre (manhattan distance)"""
	distances = []
	for x in range(x_size):
		for y in range(y_size):
			if board[x][y] == 1:
				distances.append(abs(x - mid_x) + abs(y - mid_y))
	return max(distances)

def h2(board):
	""" Heuristic based on number of movable pegs. """
	count = peg_count(board)
	possible_moves = generate_moves(board)

	if len(possible_moves) == 0:
		return float('inf')

	number_of_moves = len(possible_moves)
	return count - 1 / (number_of_moves + 1)

# Comment which heursitc you wish not to uses
def heuristic(board):
	return h1(board)
print("\nh1")

# def heuristic(board):
# 	return h2(board)
# print("\nh2")


#####################################################################################################################


def priority_queue(board_list):
	""" Orders board_list into a priority queue based on the heuristic(s) used. """
	scores = [heuristic(board) for board in board_list]
	return sorted(list(zip(board_list, scores)), key=lambda x: x[1])


def a_star(board):
	print("\nStart board:")
	print(board)
	start_node = board
	p_queue = priority_queue([board])
	visited = set()
	skipped = 0
	end_states = 0

	while p_queue:
		current_node = p_queue.pop()[0]
		visited.add(board_code(current_node))
		possible_moves = generate_moves(current_node)

		if len(possible_moves) == 0:
			end_states += 1
			if is_solution(current_node):
				print("\nNodes visited:", len(visited))
				print("Nodes skipped:", skipped)
				print("End states:", end_states)
				return True

		# Update priority queue with the non-visited neighbours of current_code
		neighbours = []
		for move in possible_moves:
			neighbour = update_board(np.copy(current_node), move)
			hash_code = board_code(neighbour)

			if hash_code not in visited:
				neighbours.append(neighbour)

			else:
				skipped += 1
		p_queue = p_queue + priority_queue(neighbours)
	
	print("No solution found!")
	return None


t = perf_counter()	
a_star(board)
print("runtime:", perf_counter() - t)
r = resource.getrusage(resource.RUSAGE_SELF)
print(f'Memory usage (MB): {r.ru_maxrss / 1000000}')


