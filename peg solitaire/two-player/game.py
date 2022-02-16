from dataclasses import dataclass

@dataclass 
class State():
    '''Representation of the board game in binary.'''
    bitboard1: int = 9552747565056 #161107674112
    '''
    00000000
    00001000
    10110000
    00101100
    00100000
    00010000
    00000000
    '''
    bitboard2: int = 13546001516593184 #106103477157904
    '''
    00110000
    00100000
    00000100
    01000000
    10000110
    00000000
    00100000
    '''
    def possible_moves(self, player: bool, direction: str) -> int:
        '''Find all possible next moves given the state.'''
        if player:
            friendly_bits, enemy_bits = self.bitboard1, self.bitboard2
        else: 
            friendly_bits, enemy_bits = self.bitboard2, self.bitboard1

        overlap = self.bitboard1 | self.bitboard2
        directions = {'N': -8, 'E': 1, 'S': 8, 'W': -1}
        d = directions[direction]
        adjacent_pegs = int(friendly_bits * 2**d) & overlap
        end = int(adjacent_pegs * 2**d) & ~friendly_bits & BOARD_BIMASK
        start = int(end * 2**-(2*d)) & BOARD_BIMASK
        return start
    
    def render(self) -> None:
        '''Process and print the current state to the terminal.'''
        for row in range(ROWS):
            output_row = ''
            for n in range(COLS*row,COLS*row+COLS):
                nth_bit = 1 << n
                if BOARD_BIMASK & nth_bit:
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
        self.player = 1 # player 1 = 1, player 2 = -1
        self.state.render()
        
    def make_move(self):
        '''Applies an action.'''
        if self.player == 1:
            pass
        else:
            pass
        self.state.render()
        reward, done = self.is_game_over()
        self.player *= -1 # change player
        return

    def is_game_over(self):
        '''Checks whether any terminal states have been reached.'''
        return

    def ask_for_action(self):
        '''Asks user for players next move.'''
        return
                
    
def main():
    game = Solitaire2()
    game.state.bitboard1 = game.state.possible_moves(1,'W') 
    game.state.bitboard2 = 0
    game.state.render() 

if __name__ == "__main__":
    ROWS, COLS = 7, 8
    BOARD_BIMASK = 15825266546718776 #124141734710812 # English cross board shape
    '''
    00111000
    00111000
    11111110
    11111110
    11111110
    00111000
    00111000
    '''
    main()