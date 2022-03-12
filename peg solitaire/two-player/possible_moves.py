from random import choice
import game_logic as g

def main() -> list[int]:
    avg_moves = []
    for e in range(SIMULATIONS):
        ith_move = -1
        g.game = g.Symmetrical()
        while not g.game.state.is_terminal():
            #g.game.render()
            children = g.game.state.find_children()
            possible_moves = len(children)
            g.game.state = choice(children)
            ith_move += 1
            try:
                x = avg_moves[ith_move] * e
                x2 = (x + possible_moves) / (e+1)
                avg_moves[ith_move]=x2
            except IndexError:
                avg_moves.append(possible_moves)
    return avg_moves

if __name__ == "__main__":
    SIMULATIONS = 50000
    a = main()
    b = sum(a)/len(a)
    print(f'ith possible moves: {a}')
    print(f'branching factor: {b}')