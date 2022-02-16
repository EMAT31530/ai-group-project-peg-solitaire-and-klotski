from dataclasses import dataclass
import mailbox

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
    
    def mailbox(self) -> list[str]:
        '''Convert the state into mailbox representation.'''
        output = ''
        for n in range(BYTE_LENGTH):
            nth_bit = 1 << n
            if BOARD_BIMASK & nth_bit:
                peg = (self.bitboard1 & nth_bit and 1) + 2*(self.bitboard2 & nth_bit and 1)
                output+=str(peg)
            else:
                output+='-'
        return output
    
    def make2D(self) -> list[list]:
        '''Remove bitboard row seperator bits and split it by the number of rows.'''
        mailbox = self.mailbox()
        return [ mailbox[ HEIGHT*row : HEIGHT*row+HEIGHT ] for row in range(WIDTH) ]

class Solitaire2():
    '''A two-player peg solitaire game class.'''
    def __init__(self):
        self.state = State()
        self.player = 1 # player 1 = 1, player 2 = -1
        self.render()
        
    def make_move(self):
        '''Applies an action.'''
        if self.player == 1:
            pass
        else:
            pass
        self.render()
        reward, done = self.is_game_over()
        self.player *= -1 # change player
        return
    
    def render(self) -> None:
        '''Processes and prints the current state to the terminal.'''
        twoD = self.state.make2D()
        for r in twoD:
            print(r)

    def is_game_over(self):
        '''Checks whether any terminal states have been reached.'''
        return

    def ask_for_action(self):
        '''Asks user for players next move.'''
        return
                
    
def main():
    game = Solitaire2()
    game.render()

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