'''Two-player Monte Carlo tree search using UCT algorithm.'''

from math import log, sqrt
from random import choice
from game_logic import game, Node
    
def uct_search(root: Node, iterations: int = 50) -> Node: 
    '''Build a game tree starting from the `root` node using UCT and return the best performing successor.
    `Iterations` corresponds to how many random playouts will be performed.'''
    root.parent = None # prevents backup of nodes that came before the new root node
    while iterations:
        iterations -= 1
        leaf = tree_policy(root)
        reward = default_policy(leaf)
        backup(leaf, reward)
    return select(root, 0)

def tree_policy(node: Node) -> Node:
    'Traverse down the game tree from the root node until a leaf node is found.'
    while not node.is_terminal():
        if not node.children:
            return expand(node)
        else:
            node = select(node, C)
    return node

def expand(node: Node) -> Node:
    'Add unexplored children nodes to the tree and return one such child at random.'
    children = node.find_children()
    return choice(children)

def select(node: Node, c: float) -> Node:
    'Select the best child `node` using UCB1, to balance exploration and exploitation.'
    if node.player == 1:
        best_child = max(node.children, key = lambda child: child.Q / child.N + c * sqrt(2 * log(node.N) / child.N) if child.N != 0 else float('inf'))
    else:
        best_child = min(node.children, key = lambda child: child.Q / child.N - c * sqrt(2 * log(node.N) / child.N) if child.N != 0 else float('-inf'))
    return best_child

def default_policy(node: Node) -> int:
    'Randomly play from the leaf `node` until a terminal node is reached and return the reward.'
    while not node.is_terminal():
        node = node.find_random_child()
    return node.reward()

def backup(node: Node, reward: int) -> None:
    'Update the node statistics starting from the leaf node up to the root node.'
    while node:
        node.N += 1
        node.Q += reward
        node = node.parent
    return

if __name__ == '__main__':
    C = 1 # exploration weight
    default = game #
    default.state.bitboards = [0,0]
    game = default
    s1 = uct_search(root=game.state, iterations=200)
    s2 = uct_search(root=s1, iterations=200)
    pass