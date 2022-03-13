'''Two-player Monte Carlo tree search using UCT algorithm.'''

from math import log, sqrt
from random import choice
import game_logic as g
from time import perf_counter, sleep
import resource

def uct_search(root: g.Node, iterations: int = 50) -> g.Node: 
    '''Build a game tree starting from the `root` node using UCT and return the best performing successor.
    `Iterations` corresponds to how many random playouts will be performed.'''
    root.parent = None # prevents backup of nodes that came before the new root node
    #root.children = [] # so that information isn't shared between turns
    while iterations:
        iterations -= 1
        leaf = tree_policy(root)
        reward = default_policy(leaf)
        backup(leaf, reward)
    return max(root.children, key = lambda child: child.N) # select(root, 0)

def tree_policy(node: g.Node) -> g.Node:
    'Traverse down the game tree from the root node until a leaf node is found.'
    while not node.is_terminal():
        if not node.children:
            return expand(node)
        else:
            node = select(node, C)
    return node

def expand(node: g.Node) -> g.Node:
    'Add unexplored children nodes to the tree and return one such child at random.'
    children = node.find_children()
    return choice(children)

def select(node: g.Node, c: float) -> g.Node:
    'Select the best child `node` using UCB1, to balance exploration and exploitation.'
    if node.player == 1:
        best_child = max(node.children, key = lambda child: child.Q / child.N + c * sqrt(2 * log(node.N) / child.N) if child.N != 0 else float('inf'))
    else:
        best_child = min(node.children, key = lambda child: child.Q / child.N - c * sqrt(2 * log(node.N) / child.N) if child.N != 0 else float('-inf'))
    return best_child

def select2(node: g.Node, c: float) -> g.Node:
    'Alternative to `select` function in which ties between the best children are broken randomly.'
    v = []
    for child in node.children:
        if node.player == 1:
            child.v = child.Q / child.N + c * sqrt(2 * log(node.N) / child.N) if child.N != 0 else float('inf')
        else:
            child.v = child.Q / child.N - c * sqrt(2 * log(node.N) / child.N) if child.N != 0 else float('-inf')
        v.append(child.v)
    if node.player == 1:
        best_children = [child for child in node.children if child.v == max(v)]
    else:
        best_children = [child for child in node.children if child.v == min(v)]
    random_best = choice(best_children)
    return random_best

def default_policy(node: g.Node) -> int:
    'Randomly play from the leaf `node` until a terminal node is reached and return the reward.'
    while not node.is_terminal():
        node = node.find_random_child()
    return node.reward()

def backup(node: g.Node, reward: int) -> None:
    'Update the node statistics starting from the leaf node up to the root node.'
    while node:
        node.N += 1
        node.Q += reward
        node = node.parent
    return

def main(AGENT: bool, EPISODES: int, ITERATIONS: int):
    rewards = []
    t1 = perf_counter()
    for _ in range(EPISODES):
        g.game = g.LargeSymmetrical()
        while not g.game.state.is_terminal():
            if AGENT:
                g.game.state = uct_search(g.game.state, ITERATIONS)
            else:
                g.game.state = g.game.state.find_random_child()
            #AGENT = not AGENT
            #g.game.render()
            #sleep(0.1)
        rewards.append(g.game.state.reward())
    t2 = perf_counter()
    win_rate = rewards.count(1)/len(rewards)
    print(f'Player 1 win percentage: {win_rate}, Time (seconds) per game: {(t2-t1)/EPISODES}\nExploration weight: {C}, episodes: {EPISODES}, iterations: {ITERATIONS}, pattern: {g.game.__class__}')
    return

if __name__ == '__main__':
    C = 1 # exploration weight
    main(True, 500, 800)
    r = resource.getrusage(resource.RUSAGE_SELF)
    print(f'Memory usage (MB): {r.ru_maxrss / 1000000}')
    