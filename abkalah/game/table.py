from abkalah.agent.evaluate import evaluate

class TTable:
  def __init__(self):
    self.table = []

  def get(self, player, board):
    hash = self._hash(board, player)

    if (board, player) not in self.table:
      self.table[hash] = evaluate(board, player)

    return self.table[hash]
  
  def put(self, player, board, value):
    self.table[self._hash(board, player)] = value

  # TODO: given p1 and p2 stones, remove all evaluations which
  # have less stones since they can't be reached anymore
  def clean(self, p1_stones, p2_stones):
    pass

  # TODO: remove all evaluations
  def reset(self):
    pass

  # TODO
  def _hash(self, player, board):
    return 0
