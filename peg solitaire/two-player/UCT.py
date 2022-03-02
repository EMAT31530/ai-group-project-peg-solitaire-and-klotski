from collections import defaultdict
import math
from random import choice, shuffle

ROWS, COLS = 7, 8
DIRECTIONS = [-COLS, 1, COLS, -1] # N,E,S,W
BOARD_BITMASK = 0b00011100000111000111111101111111011111110001110000011100
DEFAULT_BOARD1 = 0b00001100000001000001001100110110011001000001000000011000
DEFAULT_BOARD2 = 0b10000000110000110110001000001000110110000110000000100

class Node():
    'A bitboard representation of a two-player peg solitaire board state.'
    def __init__(self, bitboard1: int, bitboard2: int, current_player: bool) -> None:
        self.bitboards = [bitboard2, bitboard1]
        self.player = current_player # player 1 = True, player 2 = False
        #render(bitboard1, bitboard2, 'node created')

    def find_children(self) -> set:
        'All possible successors of this board state.'
        print('Finding children nodes')
        successors = []
        for direction in DIRECTIONS:
            legal_ends = self._legal_move_ends(self.bitboards[self.player], direction)
            if legal_ends:
                split_ends = self._split(legal_ends)
                for end in split_ends:
                    successors.append( self._successor(end, direction) )
        if not successors: 
            successors.append( Node(self.bitboards[1], self.bitboards[0], not self.player) )
        return set(successors)

    def find_random_child(self):
        'Random successor `node` of this board state.'
        print('Random child')
        directions = DIRECTIONS.copy()
        while directions:
            shuffle(directions)
            random_direction = directions.pop()
            legal_ends = self._legal_move_ends(self.bitboards[self.player],random_direction)
            if legal_ends:
                split_ends = self._split(legal_ends)
                random_end = choice(split_ends)
                return self._successor(random_end, random_direction)
        return Node(self.bitboards[1], self.bitboards[0], not self.player) # if current player has no moves, turn is skipped
    
    def _legal_move_ends(self, bitboard: int, direction: int) -> int:
        '''Get the ending squares of all legal moves from a players' `bitboard` in a `direction`. 
        The on-bits in the returned integer represent where a players' pegs can move to.'''
        adjacent_pegs = self._bitshift(bitboard, direction) & (self.bitboards[0] | self.bitboards[1])
        legal_ends = self._bitshift(adjacent_pegs, direction) & ~bitboard & BOARD_BITMASK
        return legal_ends

    def is_terminal(self) -> bool:
        'Returns True if the node has no children. Meaning that both players have no legal moves.'
        for p in [self.player, not self.player]:
            for d in DIRECTIONS:
                legal_ends = self._legal_move_ends(self.bitboards[p], d)
                if legal_ends:
                    return False
        return True

    def reward(self) -> bool:
        'Assuming `self` is a terminal node, the player with the fewest pegs on the board wins. A tie gives player 2 the win.'
        tally1 = self.bitboards[1].bit_count()
        tally2 = self.bitboards[0].bit_count()
        if tally2 <= tally1:
            return 0 # player 2 wins
        else:
            return 1 # player 1 wins

    def _successor(self, move_end: int, direction: int): 
        'Create a successor `node` given the ending square of the move and the `direction` it was moved.'
        # Dilate twice the on-bits of a binary number in a direction
        if direction < 0:
            direction = -direction
            end_to_start = move_end | (move_end << direction) | (move_end << 2*direction)
        else:
            end_to_start = move_end | (move_end >> direction) | (move_end >> 2*direction)
        # remove affected pegs from both bitboards
        bitboard1 = self.bitboards[1] & ~end_to_start
        bitboard2 = self.bitboards[0] & ~end_to_start
        # add peg to ending square of the move
        if self.player == 1:
            bitboard1 |= move_end
        else:
            bitboard2 |= move_end
        return Node(bitboard1, bitboard2, not self.player)
    
    @staticmethod
    def _bitshift(binary: int, offset: int) -> int:
        'Does right or left bitshift depending on sign of `offset`.'
        if offset < 0:
            return binary >> -offset
        else:
            return binary << offset

    @staticmethod
    def _split(legal_moves: int) -> list[int]:
        'Split `legal moves` into invidual moves by the on-bits.'
        seperate_moves = []
        while legal_moves:
            seperate_moves.append(legal_moves & -legal_moves) # get least significant on-bit
            legal_moves &= legal_moves-1 # remove least significant on-bit
        return seperate_moves

    def __hash__(self) -> int:
        return hash((self.bitboards[0], self.bitboards[1], self.player))# alternative self.bitboards[0] | self.bitboards[1]

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.bitboards == other.bitboards
        else:
            return NotImplemented

class UCT:
    'Monte Carlo tree search using UCT algorithm. First rollout the tree then choose a move.'
    def __init__(self, C=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count of each node
        self.children = dict()  # children of each node
        self.C = C # exploration weight

    def choose(self, node: Node):
        'Choose the best successor of node. (Choose a move in the game)'
        print('Choosing best successor')
        if node.is_terminal():
            raise RuntimeError(f'choose called on terminal node {node}')
        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float('-inf')  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node: Node):
        'Make the tree one layer better. (Train for one iteration.)'
        print('Doing another iteration of rollout')
        path = self._tree_policy(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._default_policy(leaf)
        self._backup(path, reward)

    def _tree_policy(self, node: Node):
        'Find an unexplored descendent of `node`.'
        print('finding unexplored child node')
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]: # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._best_child(node)  # descend a layer deeper

    def _expand(self, node: Node):
        'Update the `tree` dict with the tree of `node`.'
        print('expanding')
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _default_policy(self, node: Node):
        'Returns the reward for a random simulation (to completion) of `node`.'
        print('Starting random simulation')
        invert_reward = True
        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backup(self, path, reward):
        'Send the reward back up to the ancestors of the leaf.'
        print('backing up')
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _best_child(self, node: Node):
        '''Select the best child `node`, balancing exploration & exploitation. 
        All children should already be expanded.'''
        print('selecting best child node')
        assert all(n in self.children for n in self.children[node])
        log_N_vertex = math.log(self.N[node])
        return max(self.children[node], key = lambda n: self.Q[n] / self.N[n] + self.C * math.sqrt(log_N_vertex / self.N[n]))

def render(bitboard1: int = 0, bitboard2: int = 0, message: str = '') -> None:
    'Print the bitboards in colour.'
    for row in range(ROWS):
        output_row = ''
        for n in range(COLS*row,COLS*row+COLS):
            nth_bit = 1 << n
            if BOARD_BITMASK & nth_bit: # if on the board
                peg = (bitboard1 & nth_bit and 1) + 2*(bitboard2 & nth_bit and 1)
                if peg == 0: # empty peg
                    output_row += '\033[39m o' # white circle
                elif peg == 1: # player 1 peg
                    output_row += '\033[34m o' # blue circle
                elif peg == 2: # player 2 peg
                    output_row += '\033[31m o' # red circle
                else:
                    raise ValueError('State not valid') 
            else: # not on the board
                if bitboard1 & nth_bit:
                    output_row += '\033[32m -' # green
                elif bitboard2 & nth_bit:
                    output_row += '\033[35m -' # magenta
                else: # no bugs
                    output_row += '\033[39m -' # white
        print(output_row)
    print(f'{message}\n')
    return

def train(rollouts: int, tree: UCT = UCT(), state: Node = Node(DEFAULT_BOARD1, DEFAULT_BOARD2, 1)):
    'Train for how many `rollouts`.'
    for _ in range(rollouts):
        tree.do_rollout(state)
        state = tree.choose(state)
        if state.is_terminal():
            break
    print(tree)

if __name__ == '__main__':
    train(5)
    pass
