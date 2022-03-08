from statistics import mean
import game_logic as g
from time import perf_counter

def main() -> list[int]:
    rewards = []
    game_lengths = []
    for _ in range(50000):
        game_length = 0
        g.game = g.DefaultBoard()
        while not g.game.state.is_terminal():
            # g.game.render()
            game_length += 1
            g.game.state = g.game.state.find_random_child()
        rewards.append( g.game.state.reward())
        game_lengths.append(game_length)
    return rewards, game_lengths

if __name__ == "__main__":
    t1 = perf_counter()
    outcomes, lengths = main()
    t2 = perf_counter()
    win_rate = outcomes.count(1)/len(outcomes)
    avg_length = mean(lengths)
    print(f'Player 1 win percentage: {win_rate}\nTime: {t2-t1}, Mean game length: {avg_length}')