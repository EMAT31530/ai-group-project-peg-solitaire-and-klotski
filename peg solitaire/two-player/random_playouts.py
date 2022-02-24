import random
import game as g
from time import sleep

def main() -> list[int]:
    rewards = []
    for _ in range(2):
        game = g.Solitaire2(display=True)
        while not game.done:
            if game.player_moves:
                rand_dir = random.choice(list(game.all_legal_moves(game.player_moves)))
                rand_legal_moves = game.player_moves[rand_dir]
                rand_square = random.choice(game.on_bits(rand_legal_moves))
            game.step(rand_dir, rand_square)
            sleep(1)
        rewards.append(game.done)
    return rewards

if __name__ == "__main__":
    r = main()
    p = r.count(1)/len(r)
    print(f'player 1 win percentage: {p}')