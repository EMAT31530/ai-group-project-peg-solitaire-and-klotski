from dataclasses import dataclass

@dataclass 
class State():
    '''Representation of the board game in binary.'''
    bitboard1: int = 0
    bitboard2: int = 0

    def possible_moves(self) -> int:
        '''Find all possible next moves given the state.'''
        return
    
    def mailbox(self) -> list[int]:
        '''Convert the state into mailbox representation.'''
        # (int & 1 << n and 1) gets the n'th bit of an int
        return [ (self.bitboard1 & (1 << n) and 1) + 2*(self.bitboard2 & (1 << n) and 1) for n in range(BYTE_LENGTH-1,-1,-1) ]

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
    main()