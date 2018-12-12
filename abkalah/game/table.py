from abkalah.agent.evaluate import evaluate

class TTable:
  def __init__(self):
    self.table = {}

  def get(self, board, player):
    key = tuple(board.state)

    if key not in self.table:
      self.table[key] = (board.state, evaluate(board, player))

    return self.table[key][1]
  
  def put(self, board, player, value):
    key = tuple(board.state)

    if key not in self.table:
      self.table[key] = (board.state, evaluate(board, player))
    else:
      self.table[key] = (board.state, value)
    
    return value

  def clean(self, p1_stones, p2_stones):
    self.table = dict(filter(lambda n: n[0][7] >= p1_stones and n[0][15] >= p2_stones, self.table.items()))

  # TODO: remove all evaluations
  def reset(self):
    self.table = {}

    return 0
