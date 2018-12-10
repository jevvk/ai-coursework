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

  def search(self, board, depth, maximising, alpha = float('-inf'), beta = float('inf'), first=False):
    global mem

    node = Node()

    if depth == 0:
      node.value = evaluate(board, self.side)
      return node
    
    if maximising:
      player = self.side
      moves = board.available_moves(player)
      # TODO: order moves by previous valuation (transposition table)

      if self.terminal_test(board, moves):
        node.value = evaluate(board, self.side)
        return node
      
      node.value = float('-inf')

      for move in moves:
        if mem['ab_break']: break
        
        new_board, new_player = board.move(move)
        value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta).value

        # if first: print('trying', new_board.state, node.value)

        if (node.value < value):
          # if first: print('maxmising', new_board.state, 'new', value, move)
          node.value = value
          node.move = move

        alpha = max(alpha, node.value)

        if beta <= alpha: break
    else:
      player = NORTH if self.side == SOUTH else SOUTH
      moves = board.available_moves(player)
      # TODO: order moves by previous valuation (transposition table)

      if self.terminal_test(board, moves):
        node.value = evaluate(board, self.side)

      node.value = float('inf')

      for move in moves:        
        if mem['ab_break']: break
        
        new_board, new_player = board.move(move)
        value = self.search(new_board, depth - 1, new_player == self.side, alpha, beta).value

        # if first: print('trying', new_board.state, node.value)

        if (node.value > value):
          # if first: print('minimising', new_board.state, 'new', value, move)
          node.value = value
          node.move = move

        beta = min(beta, node.value)

        if beta <= alpha: break

    # if first: print('first', node.value, node.move)

    return node

  def terminal_test(self, board, moves):
    for move in moves:
      new_board, _ = board.move(move)

      if new_board.is_end():
        return True

    return False

