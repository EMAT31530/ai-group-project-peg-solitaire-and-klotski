ROWS, COLS = 7, 8
BOARD_BITMASK = 0b00011100000111000111111101111111011111110001110000011100 # English cross board shape
DIRECTIONS = {'N': -COLS, 'E': 1, 'S': COLS, 'W': -1}

class Solitaire2():
    '''A two-player peg solitaire game class.'''
    def __init__(self):
        self.bitboard1: int = 0b00001100000001000001001100110110011001000001000000011000
        self.bitboard2: int = 0b10000000110000110110001000001000110110000110000000100
        self.player = True # player 1 = True, player 2 = False
        self.overlap = self.bitboard1 | self.bitboard2

    def render(self) -> None:
        '''Process and print the current state to the terminal in colour.'''
        for row in range(ROWS):
            output_row = ''
            for n in range(COLS*row,COLS*row+COLS):
                nth_bit = 1 << n
                if BOARD_BITMASK & nth_bit: # if on the board
                    peg = (self.bitboard1 & nth_bit and 1) + 2*(self.bitboard2 & nth_bit and 1)
                    if peg == 0:
                        output_row += '\033[39m o'
                    elif peg == 1:
                                output_row += '\033[34m o'
                    elif peg == 2:
                        output_row += '\033[31m o'
                    else:
                        raise ValueError('State not valid') 
                else:
                    output_row+='\033[39m  '
            print(output_row)
        print('\n')
        return

    def is_game_over(self):
        '''Checks whether both players are unable to move, if so scores are tallied.'''
        player_moves = self.all_legal_moves(self.player)
        if not player_moves:
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
        return player_moves

    def all_legal_moves(self, player: bool) -> dict:
        '''Find legal moves in all directions for a player.'''
        if player == 1:
            player_bits = self.bitboard1
        else: 
            player_bits = self.bitboard2
        all_moves = {}
        for d in DIRECTIONS:
            moves = self.legal_moves(DIRECTIONS[d], player_bits)
            if moves:
                all_moves[d] = moves
        return all_moves
    
    def legal_moves(self, direction: int, player_bits) -> int:
        '''Find the legal moves for a player in a direction given the current board state.'''
        adjacent_pegs = int(player_bits * 2**direction) & self.overlap
        end_moves = int(adjacent_pegs * 2**direction) & ~player_bits & BOARD_BITMASK 
        start_moves = int(end_moves * 2**-(2*direction)) & BOARD_BITMASK 
        return start_moves

    def make_move(self, start: int, direction:int) -> None:
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
    def on_bits(bin: int) -> list[int]:
        '''Get all on bits from an integer.'''
        moves = []
        n = 0
        while bin:
            if bin & 1: # get least sig. bit
                moves.append(1 << n)
            n += 1
            bin >>= 1 # remove least sig. bit
        return moves

def _view(bitboard, message) -> None:
    '''Print a bitboard for debugging purposes.'''
    for row in range(ROWS):
        output_row = ''
        for n in range(COLS*row,COLS*row+COLS):
            nth_bit = 1 << n
            if BOARD_BITMASK & nth_bit: # if on the board
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