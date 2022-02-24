import random
import game as g

def main():
    rewards = []
    for playout in range(100000):
        game = g.Solitaire2()
        player_moves = game.is_game_over()
        while not game.done:
            if player_moves:
                rand_dir = random.choice(list(player_moves))
                rand_legal_moves = player_moves[rand_dir]
                rand_move = random.choice(game.on_bits(rand_legal_moves))
                game.make_move(rand_move, g.DIRECTIONS[rand_dir])
            #game.state.render()
            game.overlap = game.bitboard1 | game.bitboard2
            game.player = not game.player
            player_moves = game.is_game_over()
        rewards.append(game.done)
    return rewards

if __name__ == "__main__":
    
    r = main()
    p = r.count(1)/len(r)
    print(f'player 1 win percentage: {p}')