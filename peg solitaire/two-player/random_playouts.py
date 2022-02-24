import random
import game as g
from time import sleep

def main() -> list[int]:
    rewards = []
    for _ in range(2):
        game = g.Solitaire2(display=True)
        while not game.done:
            if game.player_legal_moves:
                rand_dir = random.choice(list(game.player_legal_moves))
                seperate_moves = game.on_bits(game.player_legal_moves[rand_dir])
            game.step(rand_dir, random.choice(seperate_moves))
            sleep(1)
        rewards.append(game.done)
    return rewards

if __name__ == "__main__":
    outcomes = main()
    win_rate = outcomes.count(1)/len(outcomes)
    print(f'player 1 win percentage: {win_rate}')