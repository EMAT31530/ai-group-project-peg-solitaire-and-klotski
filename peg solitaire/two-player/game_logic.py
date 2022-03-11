'''
Create objects to control the logic of a two-player peg solitaire game. 
'''

from random import choice, shuffle

class Node:
    'A bitboard representation of the board game state.'
    def __init__(self, player: bool, bitboards: list[int], parent: object = None) -> None:
        self.bitboards = bitboards # index 1 corresponds to the bitboard of player 1
        self.player = player # player 1 = True, player 2 = False
        self.parent = parent
        if parent:
            parent.children.append(self)
        self.children = []
        self.Q = 0  # total reward
        self.N = 0 # total visit count

    def find_random_child(self) -> object:
        'Randomly return a legal successor node.'
        directions = game.DIRECTIONS.copy()
        while directions:
            shuffle(directions)
            random_direction = directions.pop()
            legal_ends = self._legal_move_ends(self.bitboards[self.player],random_direction)
            if legal_ends:
                split_ends = self._split(legal_ends)
                random_end = choice(split_ends)
                random_successor = self._successor(random_end, random_direction)
                return Node(player=not self.player, bitboards=random_successor)
        return Node(player=not self.player, bitboards=self.bitboards) # if current player has no moves, turn is skipped

    def find_children(self) -> list[object]:
        'Find all possible successors of this `node`. Nodes are updated with who their parent and children are.'
        for direction in game.DIRECTIONS:
            legal_ends = self._legal_move_ends(self.bitboards[self.player], direction)
            if legal_ends:
                split_ends = self._split(legal_ends)
                for end in split_ends:
                    successor = self._successor(end, direction)
                    Node(parent=self, player=not self.player, bitboards=successor)
        if not self.children: # if current player has no moves, turn is skipped
            Node(parent=self, player=not self.player, bitboards=self.bitboards)
        return self.children

    def is_terminal(self) -> bool:
        'Returns True if the node has no children. Meaning that both players have no legal moves.'
        for p in [self.player, not self.player]:
            for d in game.DIRECTIONS:
                legal_ends = self._legal_move_ends(self.bitboards[p], d)
                if legal_ends:
                    return False
        return True

    def reward(self) -> int:
        '''Assuming `self` is a terminal node, return a `reward` of 1 if player 1 wins and -1 otherwise. 
        The player with the fewest pegs on the board wins, a tie gives player 2 the win.'''
        tally1 = self.bitboards[1].bit_count()
        tally2 = self.bitboards[0].bit_count()
        if tally2 <= tally1:
            return -1 # player 2 wins
        else:
            return 1 # player 1 wins

    def _successor(self, move_end: int, direction: int) -> tuple[int]: 
        'Return the successor state bitboards given the ending square of the move and the direction it was moved.'
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
        return bits2, bits1
    
    def _legal_move_ends(self, bitboard: int, direction: int) -> int:
        '''Get the ending squares of all legal moves from a players' `bitboard` in a `direction`. 
        The on-bits in the returned integer represent where a players' pegs can move to.'''
        adjacent_pegs = self._bitshift(bitboard, direction) & (self.bitboards[0] | self.bitboards[1])
        legal_ends = self._bitshift(adjacent_pegs, direction) & ~bitboard
        return legal_ends
    
    @staticmethod
    def _bitshift(binary: int, offset: int) -> int:
        'Does right or left bitshift depending on sign of `offset`.'
        if offset < 0:
            return (binary >> -offset) & game.BITMASK
        else:
            return (binary << offset) & game.BITMASK

    @staticmethod
    def _split(legal_moves: int) -> list[int]:
        'Split `legal moves` into invidual moves by the on-bits.'
        seperate_moves = []
        while legal_moves:
            seperate_moves.append(legal_moves & -legal_moves) # get least significant on-bit
            legal_moves &= legal_moves - 1 # remove least significant on-bit
        return seperate_moves

class Solitaire2:
    'Game object that defines the board shape and starting position.'
    def __init__(self, rows: int, cols: int, shape: int, state: Node) -> None:
        self.ROWS = rows
        self.COLS = cols
        self.BITMASK = shape # used to delete pieces that move off the board
        self.DIRECTIONS = [-cols, 1, cols, -1] # N,E,S,W
        self.state = state
        
    def render(self, message: str = '') -> None:
        'Print the bitboards in colour, mainly used for debugging.'
        for row in range(self.ROWS):
            output_row = ''
            for n in range(self.COLS*row,self.COLS*row+self.COLS):
                nth_bit = 1 << n
                if nth_bit & self.BITMASK: # if on the board
                    peg = (self.state.bitboards[1] & nth_bit and 1) + 2*(self.state.bitboards[0] & nth_bit and 1)
                    if peg == 0: # empty peg
                        output_row += '\033[39m o' # white circle
                    elif peg == 1: # player 1 peg
                        output_row += '\033[34m o' # blue circle
                    elif peg == 2: # player 2 peg
                        output_row += '\033[31m o' # red circle
                    else:
                        raise ValueError('State not valid') 
                else: # not on the board
                    if self.state.bitboards[1] & nth_bit:
                        output_row += '\033[32m -' # green
                    elif self.state.bitboards[0] & nth_bit:
                        output_row += '\033[35m -' # magenta
                    else: # no bugs
                        output_row += '\033[39m -' # white
            print(output_row)
        print(f'{message}\n')
        return

class Symmetrical(Solitaire2):
    'Default version of the two-player peg solitaire game board. 7x7 board with symmetrical pattern.'
    def __init__(self) -> None:
        super().__init__(7,8,7912633273359388,Node(player=True, bitboards=[13004381212,7912620134760448]))

class Weave(Solitaire2):
    '7x7 board with weave pattern.'
    def __init__(self) -> None:
        super().__init__(7,8,7912633273359388,Node(player=True, bitboards=[1147964584367120,6755871891324940]))

class Spiral(Solitaire2):
    '7x7 board with spiral pattern.'
    def __init__(self) -> None:
        super().__init__(7,8,7912633273359388,Node(player=True, bitboards=[3382180283944984,4530452855196676]))

class Lattice(Solitaire2):
    '7x7 board with lattice pattern.'
    def __init__(self) -> None:
        super().__init__(7,8,7912633273359388,Node(player=True, bitboards=[2273971863688200,5638661275453460]))

class LargeSymmetrical(Solitaire2):
    '11x11 board with symmetrical pattern.'
    def __init__(self) -> None:
        super().__init__(11,12,329729043244155137334757505615730278648,Node(player=True, bitboards=[135470563070413004728140024,329729043244019666734793604463583035392]))

class LargeWeave(Solitaire2):
    '11x11 board with weave pattern.'
    def __init__(self) -> None:
        super().__init__(11,12,329729043244155137334757505615730278648,Node(player=True, bitboards=[85096554508585988530613290924595544080,244577969605362733784117297916730671336]))

class LargeStripes(Solitaire2):
    '11x11 board with stripe pattern.'
    def __init__(self) -> None:
        super().__init__(11,12,329729043244155137334757505615730278648,Node(player=True, bitboards=[329648562603253106702466487593665036536,80480640902030595397529874646138880]))

class LargeLattice(Solitaire2):
    '11x11 board with lattice pattern.'
    def __init__(self) -> None:
        super().__init__(11,12,329729043244155137334757505615730278648,Node(player=True, bitboards=[223336278112896005310645686125113704616,106392765131259131987218331343197470800]))

game = None
if __name__ == '__main__':
    game = Symmetrical().render()
