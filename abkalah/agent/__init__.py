import sys
import time

from threading import Thread

from abkalah import ab_break, ab_lock, best_move, NORTH, SOUTH
from abkalah.game.board import Board

class Agent:
  def __init__(self):
    self.board = Board()
    self.side = -1
    self.playing = False
    self.ab = None

  def receive(self, message):
    global best_move, ab_break, ab_lock

    if message[:5] == 'START':
      self.side = NORTH if message[6] == 'N' else SOUTH
      self.playing = self.side == SOUTH

      while self.playing: self._play()

      self._start_ab()

    elif message[:6] == 'CHANGE':
      # break search and wait for result
      self._wait_for_ab(0)

      if message[7:11] == 'SWAP':
        self.side = NORTH
        self.playing = True

        while self.playing: self._play()

        self._start_ab()
      else:
        # update board with opponent move
        op_side = NORTH if self.side == SOUTH else SOUTH
        move = int(message[7])
        move = move if op_side == NORTH else 14 - move

        # update board while the opponent is playing
        next_player = 0

        while next_player != self.side:
          self.board, next_player = self.board.move(move)

        # play while 
        self.playing = True

        while self.playing: self._play()

        # start search
        self._start_ab()

    else: # END
      self._wait_for_ab(0)

      sys.exit(0)
  
  def _start_ab(self):
    self.ab = Thread(target=self.calculate)
    self.ab.start()

  def _wait_for_ab(self, seconds):
    global best_move, ab_break, ab_lock

    if seconds > 0:
      time.sleep(seconds)

    # break search and wait for result
    ab_break = True
    ab_lock.acquire()
    ab_lock.release()
  
  def _play(self):
    # interative depth search
    self._start_ab()
    self._wait_for_ab(1) # TODO
    
    next_move = best_move if self.side == NORTH else 14 - best_move

    # send message to stdout
    sys.stdout.write('MOVE;' + str(next_move) + '\n')
    sys.stdout.flush()

    # update board with our move
    self.board, next_player = self.board.move(best_move)
    self.playing = next_player == self.side

  def calculate(self):
    global best_move, ab_break, ab_lock

    ab_lock.acquire()

    # depth = 5

    # while not ab_break:
    #   ab.search(self.board, depth, maximizing=self.playing)

    best_move = 1 if self.side == NORTH else 9

    ab_lock.release()
