'''Two-player Monte Carlo tree search using UCT algorithm.'''

from math import log, sqrt
from random import choice
import game_logic as g
from time import perf_counter
    
def uct_search(root: g.Node, iterations: int = 50) -> g.Node: 
    '''Build a game tree starting from the `root` node using UCT and return the best performing successor.
    `Iterations` corresponds to how many random playouts will be performed.'''
    root.parent = None # prevents backup of nodes that came before the new root node
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

if __name__ == '__main__':
    C = 1 # exploration weight
    agent = True # uct = True, random = false
    rewards = []
    #g.game.render()
    episodes = 100
    t1 = perf_counter()
    for _ in range(episodes):
        g.game = g.Spiral()
        while not g.game.state.is_terminal():
            if agent:
                g.game.state = uct_search(g.game.state, 100)
            else:
                g.game.state = g.game.state.find_random_child()
            agent = not agent
            #g.game.render()
        rewards.append(g.game.state.reward())

    t2 = perf_counter()
    win_rate = rewards.count(1)/len(rewards)
    print(f'Player 1 win percentage: {win_rate}\nTime: {(t2-t1)/episodes} seconds per game')