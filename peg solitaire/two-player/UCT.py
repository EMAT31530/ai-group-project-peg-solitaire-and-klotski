from random import choice, shuffle
from math import log, sqrt

ROWS, COLS = 7, 8
DIRECTIONS = [-COLS, 1, COLS, -1] # N,E,S,W
BOARD_BITMASK = 0b00011100000111000111111101111111011111110001110000011100
RENDER = False

def render(bitboard1: int = 0, bitboard2: int = 0, message: str = '') -> None:
    'Print the bitboards in colour, mainly used for debugging.'
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

class Node():
    'A bitboard representation of a two-player peg solitaire game board state.'
    def __init__(self, player: bool = True, parent: object = None, bitboard1: int = 0b00001100000001000001001100110110011001000001000000011000, bitboard2: int = 0b10000000110000110110001000001000110110000110000000100) -> None:
        self.bitboards = [bitboard2, bitboard1]
        self.player = player # player 1 = True, player 2 = False
        self.parent = parent
        if parent:
            parent.children.append(self)
        self.children = []
        self.Q = 0  # total reward
        self.N = 0 # total visit count
        if RENDER:
            render(bitboard1, bitboard2, 'node created')

    def find_random_child(self):
        'Return successor `node` in randomised direction and board square.'
        directions = DIRECTIONS.copy()
        while directions:
            shuffle(directions)
            random_direction = directions.pop()
            legal_ends = self._legal_move_ends(self.bitboards[self.player],random_direction)
            if legal_ends:
                split_ends = self._split(legal_ends)
                random_end = choice(split_ends)
                return self._successor(random_end, random_direction, None)
        return Node(player=not self.player, parent=None, bitboard1=self.bitboards[1], bitboard2=self.bitboards[0]) # if current player has no moves, turn is skipped

    def find_children(self) -> list:
        'Find all possible successors of this `node`.'
        for direction in DIRECTIONS:
            legal_ends = self._legal_move_ends(self.bitboards[self.player], direction)
            if legal_ends:
                split_ends = self._split(legal_ends)
                for end in split_ends:
                    self._successor(end, direction, self)
        if not self.children: 
            Node(player=not self.player, parent=self, bitboard1=self.bitboards[1], bitboard2=self.bitboards[0])
        return self.children

    def is_terminal(self) -> bool:
        'Returns True if the node has no children. Meaning that both players have no legal moves.'
        for p in [self.player, not self.player]:
            for d in DIRECTIONS:
                legal_ends = self._legal_move_ends(self.bitboards[p], d)
                if legal_ends:
                    return False
        return True

    def reward(self):
        '''Assuming `self` is a terminal node, return a `reward` of 1 if player 1 wins and -1 otherwise. 
        The player with the fewest pegs on the board wins, a tie gives player 2 the win.'''
        tally1 = self.bitboards[1].bit_count()
        tally2 = self.bitboards[0].bit_count()
        if tally2 <= tally1:
            return -1 # player 2 wins
        else:
            return 1 # player 1 wins

    def _successor(self, move_end: int, direction: int, parent: object): 
        'Return a successor `node` given the ending square of the move and the `direction` it was moved.'
        # dilate twice the on-bits of a bitboard in a direction
        if direction < 0:
            end_to_start = move_end | (move_end << -direction) | (move_end << -2*direction)
        else:
            end_to_start = move_end | (move_end >> direction) | (move_end >> 2*direction)
        # remove affected pegs from both bitboards
        bits1 = self.bitboards[1] & ~end_to_start
        bits2 = self.bitboards[0] & ~end_to_start
        # add peg to ending square of the move
        if self.player == 1:
            bits1 |= move_end
        else:
            bits2 |= move_end
        return Node(player=not self.player, parent=parent, bitboard1=bits1, bitboard2=bits2)
    
    def _legal_move_ends(self, bitboard: int, direction: int) -> int:
        '''Get the ending squares of all legal moves from a players' `bitboard` in a `direction`. 
        The on-bits in the returned integer represent where a players' pegs can move to.'''
        adjacent_pegs = self._bitshift(bitboard, direction) & (self.bitboards[0] | self.bitboards[1])
        legal_ends = self._bitshift(adjacent_pegs, direction) & ~bitboard & BOARD_BITMASK
        return legal_ends
    
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

class UCT:
    'Two-player Monte Carlo tree search using UCT algorithm.'
    def __init__(self, C: float = 1):
        self.C = C # exploration weight
    
    def search(self, v0: Node, time: int = 50):
        while time:
            time -= 1
            vl = self.tree_policy(v0)
            reward = self.default_policy(vl)
            self.backup(vl, reward)
        return self.best_child(v0, 0)
    
    def tree_policy(self, v: Node) -> Node:
        while not v.is_terminal():
            if not v.children:
                return self.expand(v)
            else:
                v = self.best_child(v, self.C)
        return v
    
    def expand(self, v: Node) -> Node:
        'Add unexplored `node` to the `tree`, add `children` nodes to the `node` and return one such child.'
        children = v.find_children()
        return children[0]
    
    def best_child(self, v: Node, c: float) -> Node:
        'Select the best child `node`, balancing exploration & exploitation using UCB1.'
        if v.player == 1:
            best_child = max(v.children, key = lambda child: child.Q / child.N + c * sqrt(2*log(v.N) / child.N) if child.N != 0 else float('inf'))
        else:
            best_child = min(v.children, key = lambda child: child.Q / child.N - c * sqrt(2*log(v.N) / child.N) if child.N != 0 else float('-inf'))
        return best_child

    def default_policy(self, v: Node):
        'Randomly play until a terminal node is reached and return the reward.'
        while not v.is_terminal():
            v = v.find_random_child()
        return v.reward()
    
    def backup(self, v: Node, reward: int) -> None:
        'Propagate the `reward` back up the nodes in the `tree` starting from the leaf node until the root node is reached.'
        while v:
            v.N += 1
            v.Q += reward
            v = v.parent
        return


if __name__ == '__main__':
    uct = UCT()
    s0 = Node()
    s1 = uct.search(v0=s0, time=200)
    s2 = uct.search(v0=s1, time=200)
    pass