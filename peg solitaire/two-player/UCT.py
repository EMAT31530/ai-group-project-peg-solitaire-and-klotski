import math
from random import choice, shuffle

ROWS, COLS = 7, 8
DIRECTIONS = [-COLS, 1, COLS, -1] # N,E,S,W
BOARD_BITMASK = 0b00011100000111000111111101111111011111110001110000011100
DEFAULT_BOARD1 = 0b00001100000001000001001100110110011001000001000000011000
DEFAULT_BOARD2 = 0b10000000110000110110001000001000110110000110000000100

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
    'A bitboard representation of a two-player peg solitaire board state.'
    def __init__(self, bitboard1: int, bitboard2: int, current_player: bool) -> None:
        self.parent = None
        self.children = []
        self.Q = 0  # total reward
        self.N = 0 # total visit count
        self.player = current_player # player 1 = True, player 2 = False
        self.bitboards = [bitboard2, bitboard1]
        #render(bitboard1, bitboard2, 'node created')

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

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
        child = Node(bitboard1, bitboard2, not self.player)
        self.add_child(child)
        return child
    
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
    'Two-player Monte Carlo tree search using UCT algorithm.'
    def __init__(self, C=1):
        self.C = C # exploration weight
        self.tree = set()
    
    def search(self, s0: Node):
        return self.select_move(board, s0, 0)
    
    def select_move(self, board: Node, s: Node, c: int):
        return


if __name__ == '__main__':
    u = UCT()
    pass