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
    
    if maximising:
      player = self.side
      moves = board.available_moves(player)
      # TODO: order moves by previous valuation (transposition table)

      if self.terminal_test(board, moves):
        node.value = evaluate(board)
        return node
      
      for move in moves:
        if ab_break: break
        
        new_board, new_player = board.move(move)
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

      if self.terminal_test(board, moves):
        node.value = evaluate(board)
        return node

      for move in moves:
        if ab_break: break
        
        new_board, new_player = board.move(move)
        value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta).value

        if (node.value >= value):
          node.value = value
          node.move = move

        beta = min(beta, node.value)

        if beta <= alpha: break

    return node

  def terminal_test(self, board, actions):
    for action in actions:
      new_board = board.move(action)

      if new_board.is_end():
        return True

    return False

