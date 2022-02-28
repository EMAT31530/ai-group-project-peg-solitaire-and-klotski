from collections import defaultdict
import math
from random import choice, shuffle

ROWS, COLS = 7, 8
DIRECTIONS = [-COLS, 1, COLS, -1] # N,E,S,W
BOARD_BITMASK = 0b00011100000111000111111101111111011111110001110000011100

class UCT:
    'Monte Carlo tree searcher. First rollout the tree then choose a move.'

    def __init__(self, C=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count of each node
        self.tree = dict()  # children of each node
        self.C = C # exploration weight

    def choose(self, node):
        'Choose the best successor of node. (Choose a move in the game)'
        if node.is_terminal():
            raise RuntimeError(f'choose called on terminal node {node}')
        if node not in self.tree:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float('-inf')  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.tree[node], key=score)

    def do_rollout(self, node):
        'Make the tree one layer better. (Train for one iteration.)'
        path = self._tree_policy(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._default_policy(leaf)
        self._backup(path, reward)

    def _tree_policy(self, node):
        'Find an unexplored descendent of `node`'
        path = []
        while True:
            path.append(node)
            if node not in self.tree or not self.tree[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.tree[node] - self.tree.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._best_child(node)  # descend a layer deeper

    def _expand(self, node):
        'Update the `tree` dict with the tree of `node`'
        if node in self.tree:
            return  # already expanded
        self.tree[node] = node.find_tree()

    def _default_policy(self, node):
        'Returns the reward for a random simulation (to completion) of `node`'
        invert_reward = True
        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backup(self, path, reward):
        'Send the reward back up to the ancestors of the leaf.'
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _best_child(self, node):
        'Select a child of node, balancing exploration & exploitation.'

        # All tree of node should already be expanded:
        assert all(n in self.tree for n in self.tree[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            'Upper confidence bound for trees'
            return self.Q[n] / self.N[n] + self.C * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.tree[node], key=uct)


class Node():
    '''A bitboard representation of a two-player peg solitaire board state.'''
    def __init__(self, bitboard1: int, bitboard2: int, current_player: bool) -> None:
        self.bitboards = [bitboard2, bitboard1]
        self.player = current_player # player 1 = True, player 2 = False

    def find_random_child(self):
        'Random successor of this board state.'
        directions = DIRECTIONS.copy()
        while directions:
            shuffle(directions)
            random_direction = directions.pop()
            adjacent_pegs = self.bitshift(self.bitboards[self.player], random_direction) & self.__hash__()
            legal_ends = self.bitshift(adjacent_pegs, random_direction) & ~self.bitboards[self.player] & BOARD_BITMASK 
            if legal_ends:
                split_ends = self.split(legal_ends)
                random_end = choice(split_ends)
                end_to_start = self.smudge(random_end, -random_direction)
                bitboard1 = self.bitboards[1] & ~end_to_start
                bitboard2 = self.bitboards[0] & ~end_to_start
                if self.player == 1:
                    bitboard1 |= random_end
                else:
                    bitboard2 |= random_end
                return Node(bitboard1, bitboard2, not self.player)
        return None
    
    @staticmethod
    def smudge(binary: int, direction: int) -> int:
        '''Dilate twice the on-bits in a direction.'''
        if direction < 0:
            direction = -direction
            return binary | (binary >> direction) | (binary >> 2*direction)
        else:
            return binary | (binary << direction) | (binary << 2*direction)
    
    @staticmethod
    def bitshift(binary: int, offset: int) -> int:
        '''Does right or left bitshift depending on sign of offset.'''
        if offset < 0:
            offset = -offset
            return binary >> offset
        else:
            return binary << offset

    @staticmethod
    def split(legal_moves: int) -> list[int]:
        '''Split legal moves into invidual moves by the on-bits.'''
        seperate_moves = []
        n = 0
        while legal_moves:
            if legal_moves & 1: # get least sig. bit
                seperate_moves.append(1 << n)
            n += 1
            legal_moves >>= 1 # remove least sig. bit
        return seperate_moves
    
    def is_terminal(self):
        'Returns True if the node has no tree.'
        return True

    def reward(self):
        'Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc.'
        return 0

    def __hash__(self) -> int:
        return self.bitboards[0] | self.bitboards[1]

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.bitboards == other.bitboards
        else:
            return NotImplemented

n = Node(0,0,0)
a = n.smudge(0b10000000,-3)
print(bin(a))