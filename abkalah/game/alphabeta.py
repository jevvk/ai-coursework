from abkalah import d_lock

class Node:
  def __init__(self):
    pass

class AlphaBeta:
  queue = []

  def __init__(self):
    pass

  def search(self):
    while len(self.queue) > 0:
      d_lock.acquire()

      node = self.queue.pop()

      # TODO
      
      for child in node.children:
        self.queue.append(child)

      d_lock.release()
