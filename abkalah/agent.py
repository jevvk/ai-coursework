import sys
import time
from threading import Thread

from abkalah import ab_break, ab_lock, best_move
from abkalah.game.board import Board

class Agent:
  def __init__(self):
    self.board = Board()
    self.side = -1
    self.playing = False
    self.ab = None

  def receive(self, message):
    if message[:5] == 'START':
      self.side = 1 if message[6] == 'N' else 2
      self.playing = self.side == 1

      # iterative depth search
      self.ab = Thread(target=self.calculate)
      self.ab.start()
    elif message[:6] == 'CHANGE':
      global best_move, ab_break, ab_lock

      # break search and wait for result
      ab_break = True
      ab_lock.acquire()
      ab_lock.release()

      if message[7:] == 'SWAP':
        self.side = 2 if self.side == 1 else 1
        self.playing = not self.playing

      # update board with opponent move
      op_side = (self.side + 1) % 2
      move = int(message[7]) + (op_side - 1) * 8

      self.board = self.board.move(move)

      # interative depth search
      self.ab = Thread(target=self.calculate)
      self.ab.start()

      # break after n ms
      time.sleep(1) # TODO

      # break search and wait for result
      ab_break = True
      ab_lock.acquire()
      ab_lock.release()
      
      # send message to stdout
      sys.stdout.write('MOVE;' + str(best_move) + '\n')
      sys.stdout.flush()

      # update board with our move
      best_move = best_move - (self.side - 1) * 8

      self.board = self.board.move(best_move)

      # interative depth search
      self.ab = Thread(target=self.calculate)
      self.ab.start()
    else: # END
      ab_break = True
      ab_lock.acquire()
      ab_lock.release()
  
  def calculate(self):
    global best_move

    # TODO
    # best_move = alpha_beta(...).move
    ab_lock.acquire()

    best_move = 0

    ab_lock.release()
