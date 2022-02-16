from dataclasses import dataclass

@dataclass 
class State():
    '''Representation of the board game in binary.'''
    bitboard1: int = 161107674112
    '''
    0000000
    0000100
    1011000
    0010110
    0010000
    0001000
    0000000
    '''
    bitboard2: int = 106103477157904
    '''
    0011000
    0010000
    0000010
    0100000
    1000011
    0000000
    0010000
    '''
    def possible_moves(self) -> int:
        '''Find all possible next moves given the state.'''
        return
    
    def render(self) -> None:
        '''Process and print the current state to the terminal.'''
        for row in range(WIDTH):
            output_row = ''
            for n in range(HEIGHT*row,HEIGHT*row+HEIGHT):
                nth_bit = 1 << n
                if BOARD_BIMASK & nth_bit:
                    peg = (self.bitboard1 & nth_bit and 1) + 2*(self.bitboard2 & nth_bit and 1)
                    match peg:
                            case 0:
                                output_row += '\033[39m o'
                            case 1:
                                output_row += '\033[34m o'
                            case 2:
                                output_row += '\033[31m o'  
                else:
                    output_row+='\033[39m -'
            print(output_row)
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

if __name__ == "__main__":
    WIDTH, HEIGHT = 7, 7
    BYTE_LENGTH = WIDTH*HEIGHT
    FULL_BITMASK = 2**(BYTE_LENGTH) - 1 # used to remove extra bits from a left bitshift
    BOARD_BIMASK = 124141734710812 # English cross board shape
    '''
    0011100
    0011100
    1111111
    1111111
    1111111
    0011100
    0011100
    '''
    main()