ENGLISH_BITMASK = 0b00011100000111000111111101111111011111110001110000011100
DEFAULT_BOARD1 = 0b00001100000001000001001100110110011001000001000000011000
DEFAULT_BOARD2 = 0b10000000110000110110001000001000110110000110000000100

class Solitaire2:
    '''A two-player peg solitaire game using a bitboard implementation.'''
    def __init__(self, board1: int = DEFAULT_BOARD1, board2: int = DEFAULT_BOARD2, rows: int = 7, cols: int = 8, display: bool = False):
        self.bitboard1 = board1
        self.bitboard2 = board2
        self.ROWS = rows
        self.COLS = cols
        self.DIRECTIONS = {'N': -self.COLS, 'E': 1, 'S': self.COLS, 'W': -1}
        self.player = True # player 1 = True, player 2 = False
        self.overlap = self.bitboard1 | self.bitboard2
        self.player_legal_moves = self.is_game_over()
        self.display = display
        if self.display:
            self.render()

    def step(self, direction: str, move_start: int = None) -> None:
        if move_start:
            self.make_move(move_start, self.DIRECTIONS[direction])
            self.overlap = self.bitboard1 | self.bitboard2
        elif self.display:
            print('No move')
        self.player = not self.player
        self.player_legal_moves = self.is_game_over()
        if self.display:
            self.render()
        return

    def render(self) -> None:
        '''Process and print the current game state to the terminal in colour.'''
        for row in range(self.ROWS):
            output_row = ''
            for n in range(self.COLS*row,self.COLS*row+self.COLS):
                nth_bit = 1 << n
                if ENGLISH_BITMASK & nth_bit: # if on the board
                    peg = (self.bitboard1 & nth_bit and 1) + 2*(self.bitboard2 & nth_bit and 1)
                    if peg == 0: # empty peg
                        output_row += '\033[39m o' # white circle
                    elif peg == 1: # player 1 peg
                        output_row += '\033[34m o' # blue circle
                    elif peg == 2: # player 2 peg
                        output_row += '\033[31m o' # red circle
                    else:
                        raise ValueError('State not valid') 
                else: # not on the board
                    output_row += '  '
            print(output_row)
        print('\n')
        return

    def is_game_over(self) -> dict:
        '''Checks whether both players are unable to move, if so scores are tallied. 
        Returns all starting squares that have a legal move in a direction.'''
        player_legal_moves = self.all_legal_moves(self.player)
        if not player_legal_moves:
            opponent_moves = self.all_legal_moves(not self.player)
            if not opponent_moves:
                tally1 = self.bitboard1.bit_count()
                tally2 = self.bitboard2.bit_count()
                if tally2 <= tally1:
                    self.done = -1
                else:
                    self.done = 1
            else:
                self.done = 0
        else:
            self.done = 0
        return player_legal_moves

    def all_legal_moves(self, player: bool) -> dict:
        '''Find legal moves in all directions for a player.'''
        if player == 1:
            player_bits = self.bitboard1
        else: 
            player_bits = self.bitboard2
        all_moves = {}
        for d in self.DIRECTIONS:
            moves = self.legal_moves(self.DIRECTIONS[d], player_bits)
            if moves:
                all_moves[d] = moves
        return all_moves
    
    def legal_moves(self, direction: int, player_bits: int) -> int:
        '''Find the legal moves for a player in a direction given the current board state.'''
        adjacent_pegs = int(player_bits * 2**direction) & self.overlap
        end_moves = int(adjacent_pegs * 2**direction) & ~player_bits & ENGLISH_BITMASK 
        start_moves = int(end_moves * 2**-(2*direction)) & ENGLISH_BITMASK 
        return start_moves

    def make_move(self, start: int, direction: int) -> None:
        '''Update the board state with the move.'''
        # calculate middle and end position
        middle = int(start * 2**direction)
        end =  int(middle * 2**direction)
        # remove start, middle and end peg bits from bitboards
        self.bitboard1 &= ~(start|middle|end)
        self.bitboard2 &= ~(start|middle|end)
        # add end peg bit back into current players bitboard
        if self.player == 1:
            self.bitboard1 |= end
        else:
            self.bitboard2 |= end
        return

    @staticmethod
    def on_bits(possible_moves: int) -> list[int]:
        '''Get all on bits from a possible moves bitboard to split it into invidual moves.'''
        moves = []
        n = 0
        while possible_moves:
            if possible_moves & 1: # get least sig. bit
                moves.append(1 << n)
            n += 1
            possible_moves >>= 1 # remove least sig. bit
        return moves

def _view(bitboard: int, message: str, rows: int, cols: int) -> None:
    '''Print a bitboard for debugging purposes.'''
    for row in range(rows):
        output_row = ''
        for n in range(cols*row, cols*row + cols):
            nth_bit = 1 << n
            if ENGLISH_BITMASK & nth_bit: # if on the board
                peg = bitboard & nth_bit and 1
                if peg == 0:
                    output_row += '\033[39m o'
                elif peg == 1:
                    output_row += '\033[35m o'
            else:
                output_row+='\033[32m -'
        print(output_row)
    print(f'{message}\n')
    return