from dataclasses import dataclass
import random
import time
#import timeit

ROWS, COLS = 7, 8
BOARD_BITMASK = 7912633273359388 # English cross board shape
DIRECTIONS = {'N': -8, 'E': 1, 'S': 8, 'W': -1}
'''
00011100
00011100
01111111
01111111
01111111
00011100
00011100
'''
@dataclass 
class State():
    '''Representation of the board game in binary.'''
    bitboard1: int = 3382180283944984
    '''
    00001100
    00000100
    00010011
    00110110
    01100100
    00010000
    00011000
    '''
    bitboard2: int = ~(bitboard1|1<<27) & BOARD_BITMASK

    def render(self) -> None:
        '''Process and print the current state to the terminal.'''
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

class Solitaire2():
    '''A two-player peg solitaire game class.'''
    def __init__(self):
        self.state = State()
        self.player = 1 # player 1 = 1, player 2 = 0
        self.overlap = self.state.bitboard1 | self.state.bitboard2
        self.state.render()

    def is_game_over(self):
        '''Checks whether both players are unable to move, if so scores are tallied.'''
        player_moves = self.all_legal_moves(self.player)
        if not player_moves:
            opponent_moves = self.all_legal_moves(not self.player)
            if not opponent_moves:
                tally1 = self.state.bitboard1.bit_count()
                tally2 = self.state.bitboard2.bit_count()
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
            player_bits = self.state.bitboard1
        else: 
            player_bits = self.state.bitboard2
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
        self.state.bitboard1 &= ~(start|middle|end)
        self.state.bitboard2 &= ~(start|middle|end)
        # add end peg bit back into current players bitboard
        if self.player == 1:
            self.state.bitboard1 |= end
        else:
            self.state.bitboard2 |= end
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

def main():
    game = Solitaire2()
    player_moves = game.is_game_over()
    while not game.done:
        time.sleep(0.5)
        if player_moves:
            rand_dir = random.choice(list(player_moves))
            rand_legal_moves = player_moves[rand_dir]
            rand_move = random.choice(game.on_bits(rand_legal_moves))
            game.make_move(rand_move, DIRECTIONS[rand_dir])
        game.state.render()
        game.overlap = game.state.bitboard1 | game.state.bitboard2
        game.player = not game.player
        player_moves = game.is_game_over()
    print(f'reward: {game.done}')

if __name__ == "__main__":
    #print(timeit.timeit(stmt=testcode,number=100000))
    main()