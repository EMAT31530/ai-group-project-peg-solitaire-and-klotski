from dataclasses import dataclass
from multiprocessing.sharedctypes import Value

@dataclass 
class State():
    '''Representation of the board game in binary.'''
    bitboard1: int = 9552747565056&7912633273359388 # &... temp fix to remove bits
    '''
    00000000
    00001000
    10110000
    00101100
    00100000
    00010000
    00000000
    '''
    bitboard2: int = 13546001516593184&7912633273359388
    '''
    00110000
    00100000
    00000100
    01000000
    10000110
    00000000
    00100000
    '''

    def render(self) -> None:
        '''Process and print the current state to the terminal.'''
        for row in range(ROWS):
            output_row = ''
            for n in range(COLS*row,COLS*row+COLS):
                nth_bit = 1 << n
                if BOARD_BIMASK & nth_bit: # if on the board
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
        self.state.render()
        
    def play_turn(self):
        '''Player makes their move.'''
        if self.player == 1:
            pass
        else:
            pass
        self.state.render()
        reward, done = self.is_game_over()
        self.player = not self.player # change player
        return

    def is_game_over(self):
        '''Checks whether any terminal states have been reached.'''
        return

    def make_move(self, x:int, y:int, dir:int):
        '''Update the state with the move.'''
        start = self.convert_coord(x,y)
        start_moves, _ = self.legal_moves(dir)
        if start & start_moves:
            middle = int(start * 2**dir)
            self.state.bitboard1 &= ~(self.state.bitboard1 & middle)
            self.state.bitboard2 &= ~(self.state.bitboard2 & middle)
            end =  int(middle * 2**dir)
            if self.player == 1:
                self.state.bitboard1 ^= start
                self.state.bitboard1 |= end
            else:
                self.state.bitboard2 ^= start
                self.state.bitboard2 |= end
            self.state.render()
        else:
            raise ValueError('Illegal move!')
    
    def legal_moves(self, direction: int) -> int:
        '''Find all legal next moves in a direction given the current state and player.'''
        overlap = self.state.bitboard1 | self.state.bitboard2
        if self.player == 1:
            friendly_bits = self.state.bitboard1
        else: 
            friendly_bits = self.state.bitboard2
        self._view(friendly_bits,'friendly')
        self._view(int(friendly_bits * 2**direction),'shifted friendly')
        adjacent_pegs = int(friendly_bits * 2**direction) & overlap
        self._view(adjacent_pegs, 'adjacent')
        end_moves = int(adjacent_pegs * 2**direction) & ~friendly_bits & BOARD_BIMASK 
        start_moves = int(end_moves * 2**-(2*direction)) & BOARD_BIMASK 
        self._view(start_moves, 'start')
        self._view(end_moves, 'end')
        return start_moves, end_moves

    @staticmethod
    def convert_coord(x: int, y: int) -> int:
        '''Convert a coordinate into a bitmask'''
        if 0 <= x < COLS and 0 <= y < ROWS:
            bitmask = 1 << (x + COLS*y)
            if BOARD_BIMASK & bitmask:
                return bitmask
            else:
                raise ValueError('Coordinate not part of the board!') 
        else:
            raise ValueError('Coordinate out of bounds!')

    @staticmethod
    def _view(bitboard, message) -> None:
        '''Print a bitboard for debugging purposes.'''
        for row in range(ROWS):
            output_row = ''
            for n in range(COLS*row,COLS*row+COLS):
                nth_bit = 1 << n
                if BOARD_BIMASK & nth_bit: # if on the board
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
    game.player = not game.player
    print('West:')
    game.make_move(6,3,DIRECTIONS['W'])



if __name__ == "__main__":
    ROWS, COLS = 7, 8
    BOARD_BIMASK = 7912633273359388 # English cross board shape
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
    main()