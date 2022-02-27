import random
from statistics import mean
import game as g
from time import perf_counter
# from time import sleep

def main() -> list[int]:
    rewards = []
    game_lengths = []
    for _ in range(50000):
        game_length = 0
        game = g.Solitaire2(display=False)
        while not game.done:
            game_length += 1
            if game.player_legal_moves:
                rand_dir = random.choice(list(game.player_legal_moves))
                seperate_moves = game.on_bits(game.player_legal_moves[rand_dir])
                game.step(random.choice(seperate_moves),rand_dir)
            else:
                game.step()
        rewards.append(game.done)
        game_lengths.append(game_length)
    return rewards, game_lengths

if __name__ == "__main__":
    t1 = perf_counter()
    outcomes, lengths = main()
    t2 = perf_counter()
    win_rate = outcomes.count(1)/len(outcomes)
    avg_length = mean(lengths)
    print(f'Player 1 win percentage: {win_rate}\nTime: {t2-t1}, Mean game length: {avg_length}')