from random import choice
import game_logic as g

def main() -> list[int]:
    avg_moves = []
    visits = []
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
                x = avg_moves[ith_move] * visits[ith_move]
                visits[ith_move] += 1
                x2 = (x + possible_moves) / visits[ith_move]
                avg_moves[ith_move]=x2
            except IndexError:
                visits.append(1)
                avg_moves.append(possible_moves)
    return avg_moves

if __name__ == "__main__":
    SIMULATIONS = 50000
    a = main()
    b = sum(a)/len(a)
    print(f'ith possible moves: {a}')
    print(f'branching factor: {b}')