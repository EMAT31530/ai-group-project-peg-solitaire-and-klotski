import game as g

class Node:
    def __init__(self, state: int) -> None:
        self.parent = None
        self.children = []
        self.state = state
        self.visit_count = 0
        self.q = 0 # simulation reward
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

def UCT_search(s0: int):
    return

def tree_policy(v: Node):
    return

def expand(v: Node):
    return

def best_child(v: Node, c: int):
    return

def default_policy(s: int):
    return

def backup(v: Node, reward: int):
    while v:
        v.visit_count += 1
        v.q += reward
        reward *= -1
        v = v.parent
    return

