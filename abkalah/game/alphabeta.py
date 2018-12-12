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

  def search(self, board, depth, maximising, alpha = float('-inf'), beta = float('inf'), first_turn = False, first = False, second = False):
    global mem

    table = mem['ab_table']
    node = Node()

    if depth == 0:
      node.value = table.get(board, self.side)
      return node
    
    if maximising:
      player = self.side
      moves = board.available_moves(player)
      moves = sorted(moves, key = (lambda x: table.get(board.move(x)[0], self.side)))
      
      node.value = float('-inf')

      for move in moves:
        if mem['ab_break']: break
        
        new_board, new_player = board.move(move, first_turn=first_turn)
        value = 0

        if new_board.has_moves(new_player):
          value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta, second=first).value
        else:
          value = table.get(new_board, self.side)
          # value = evaluate(new_board, self.side)

        if (node.value < value):
          node.value = value
          node.move = move

          # update transposition table
          table.put(board, self.side, value)

        alpha = max(alpha, node.value)

        if beta <= alpha: break
    else:
      player = NORTH if self.side == SOUTH else SOUTH
      moves = board.available_moves(player)
      moves = sorted(moves, key = (lambda x: table.get(board.move(x)[0], self.side)))

      node.value = float('inf')

      for move in moves:        
        if mem['ab_break']: break
        
        new_board, new_player = board.move(move, first_turn=first_turn)
        value = 0

        if new_board.has_moves(new_player):
          value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta, second=first).value
        else:
          value = table.get(new_board, self.side)
          # value = evaluate(new_board, self.side)

        if (node.value > value):
          node.value = value
          node.move = move

          # update transposition table
          table.put(board, self.side, value)

        beta = min(beta, node.value)

        if beta <= alpha: break

    return node

