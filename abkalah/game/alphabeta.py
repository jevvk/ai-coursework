from abkalah import ab_break, ab_lock, NORTH, SOUTH

from abkalah.agent.evaluate import evaluate

class Node:
  def __init__(self):
    self.value = 0
    self.move = 0

class AlphaBeta:
  def __init__(self, side):
    self.side = side
    self.queue = []

  def search(self, board, depth, maximising, alpha = float('-inf'), beta = float('inf')):
    node = Node()

    if depth == 0:
      node.value = evaluate(board)
      return node
    
    if self.side == SOUTH:
      node.move = 10
    else:
      node.move = 5

    return node

