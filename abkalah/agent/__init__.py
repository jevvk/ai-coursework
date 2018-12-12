import sys
import time

from threading import Thread

from abkalah import mem, NORTH, SOUTH
from abkalah.game.board import Board
from abkalah.game.alphabeta import AlphaBeta

class Agent:

  def __init__(self):
    self.board = Board()
    self.side = -1
    self.playing = False
    self.ab = None
    self.first_turn = True
    self.can_swap = False

  def receive(self, message):
    if message[:5] == 'START':
      self.side = NORTH if message[6] == 'N' else SOUTH
      self.playing = self.side == SOUTH
      self.can_swap = not self.playing

      if self.playing: self._play()

      self._start_ab()
      # sys.exit(0)

    elif message[:6] == 'CHANGE':
      if message[7:11] == 'SWAP':
        self.side = NORTH if self.side == SOUTH else SOUTH
        self.playing = self.side == NORTH # only south can swap

        # also reset transition table here

        # restart program to update the side
        self._wait_for_ab(0)
        self._start_ab()

      else:
        # get move
        opponent = NORTH if self.side == SOUTH else SOUTH
        side = self.side if self.playing else opponent
        move = int(message[7]) - 1
        move = move if side == NORTH else 8 + move

        # update board with opponent move
        self.board, _ = self.board.move(move, first_turn=self.first_turn)

        # update player flag
        self.playing = message[-3:] == 'YOU'

      self.first_turn = False

      if self.playing:
        if self.can_swap:
          # always swap
          sys.stdout.write('SWAP\n')
          sys.stdout.flush()

          self.can_swap = False
        else:
          # break search and wait for result
          self._wait_for_ab(0)
          self._play()

          # start search
          self._start_ab()

    else: # END
      self._wait_for_ab(0)
      sys.exit(0)
  
  def _start_ab(self):
    self.ab = AgentThread(self.board, self.side, self.playing, self.first_turn)
    self.ab.start()

  def _wait_for_ab(self, seconds):
    global mem

    if self.ab is None:
      return

    if seconds > 0:
      time.sleep(seconds)

    # break search and wait for result
    mem['ab_break'] = True

    mem['ab_lock'].acquire()
    mem['ab_lock'].release()

    self.ab.join()
    self.ab = None
  
  def _play(self):
    global mem

    # interative depth search
    self._start_ab()
    self._wait_for_ab(2) # TODO
    
    best_move = mem['best_move']
    next_move = best_move if self.side == NORTH else best_move - 8

    # send message to stdout
    sys.stdout.write('MOVE;' + str(next_move + 1) + '\n')
    sys.stdout.flush()

class AgentThread(Thread):
  def __init__(self, board, side, playing, first_turn):
    Thread.__init__(self)

    self.board = board
    self.side = side
    self.playing = playing
    self.first_turn = first_turn

  def run(self):
    global mem

    mem['ab_lock'].acquire()

    ab = AlphaBeta(self.side)
    depth = 5
    mem['ab_break'] = False
    mem['best_move'] = -1

    while not mem['ab_break'] and depth < 15:
      next_move = ab.search(self.board, depth, self.playing, first_turn=self.first_turn).move
      
      # if next_move != -1:
      #   mem['best_move'] = next_move

      if (not mem['ab_break'] or mem['best_move'] == -1) and next_move != -1:
        mem['best_move'] = next_move

      depth += 1

    mem['ab_lock'].release()
