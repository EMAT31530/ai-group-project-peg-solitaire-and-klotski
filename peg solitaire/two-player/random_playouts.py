import game_logic as g
from time import perf_counter

def main() -> list[int]:
    rewards = []
    game_lengths = []
    for _ in range(SIMULATIONS):
        game_length = 0
        g.game = g.Symmetrical()
        while not g.game.state.is_terminal():
            g.game.render()
            game_length += 1
            g.game.state = g.game.state.find_random_child()
        rewards.append( g.game.state.reward())
        game_lengths.append(game_length)
    return rewards, game_lengths

if __name__ == "__main__":
    SIMULATIONS = 1
    t1 = perf_counter()
    outcomes, lengths = main()
    t2 = perf_counter()
    win_rate = outcomes.count(1)/SIMULATIONS
    avg_length = sum(lengths)/SIMULATIONS
    print(f'Player 1 win percentage: {win_rate}, Simulation time: {t2-t1}, Mean game length: {avg_length}')