import random
import game as g

def main() -> list[int]:
    rewards = []
    for _ in range(100):
        game = g.Solitaire2()
        player_moves = game.is_game_over()
        while not game.done:
            if player_moves:
                rand_dir = random.choice(list(player_moves))
                rand_legal_moves = player_moves[rand_dir]
                rand_square = random.choice(game.on_bits(rand_legal_moves))
            game.step(rand_square, rand_dir)
        rewards.append(game.done)
    return rewards

if __name__ == "__main__":
    r = main()
    p = r.count(1)/len(r)
    print(f'player 1 win percentage: {p}')