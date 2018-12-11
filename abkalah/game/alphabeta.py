from random import shuffle

from abkalah import mem, NORTH, SOUTH
from abkalah.agent.evaluate import evaluate

class Node:
  def __init__(self):
    self.value = 0
    self.move = -1

class AlphaBeta:
  def __init__(self, side):
    self.side = side
    self.queue = []

  def search(self, board, depth, maximising, alpha = float('-inf'), beta = float('inf'), first_turn = False):
    global mem

    node = Node()

    # TODO: sometimes it doesn't find a move, not sure why
    if depth == 0:
      node.value = evaluate(board, self.side)
      return node
    
    if maximising:
      player = self.side
      moves = board.available_moves(player)

      # TODO: order moves by previous valuation (transposition table)
      
      moves = sorted(moves, key = (lambda x, p = self.side, b = board: evaluate(b.move(x)[0], p)))
      node.value = float('-inf')

      for move in moves:
        if mem['ab_break']: break
        
        new_board, new_player = board.move(move, first_turn=first_turn)
        value = 0

        if new_board.is_end(new_player):
          value = evaluate(board, self.side)
        else:
          value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta).value

        if (node.value < value):
          node.value = value
          node.move = move

        alpha = max(alpha, node.value)

        if beta <= alpha: break
    else:
      player = NORTH if self.side == SOUTH else SOUTH
      moves = board.available_moves(player)

      # TODO: order moves by previous valuation (transposition table)

      moves = sorted(moves, key = (lambda x, p = self.side, b = board: -evaluate(b.move(x)[0], p)))
      node.value = float('inf')

      for move in moves:        
        if mem['ab_break']: break
        
        new_board, new_player = board.move(move, first_turn=first_turn)
        value = 0

        if new_board.is_end(new_player):
          value = evaluate(board, self.side)
        else:
          value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta).value

        if (node.value > value):
          node.value = value
          node.move = move

        beta = min(beta, node.value)

        if beta <= alpha: break

    return node

