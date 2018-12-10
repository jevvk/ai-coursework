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

  def receive(self, message):
    if message[:5] == 'START':
      self.side = NORTH if message[6] == 'N' else SOUTH
      self.playing = self.side == SOUTH

      if self.playing: self._play()

      self._start_ab()
      # sys.exit(0)

    elif message[:6] == 'CHANGE':
      if message[7:11] == 'SWAP':
        self.side = NORTH if self.side == SOUTH else SOUTH
        self.playing = self.side == NORTH # only south can swap

        # also reset transition table here

      else:
        # get move
        move = int(message[7]) - 1
        move = move if self.playing else 8 + move
        
        # update board with opponent move
        self.board, _ = self.board.move(move)
        # print(self.board.__str__())

        # update player flag
        self.playing = message[-3:] == 'YOU'

      if self.playing:
        # break search and wait for result
        self._wait_for_ab(0)
        self._play()

        # start search
        self._start_ab()

    else: # END
      self._wait_for_ab(0)

      sys.exit(0)
  
  def _start_ab(self):
    self.ab = AgentThread(self.board, self.side, self.playing)
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
    # print('MOVE;' + str(next_move + 1), file=log)

    # update board with our move
    # self, next_player = self.board.move(best_move)
    # self.playing = next_player == self.side

class AgentThread(Thread):
  def __init__(self, board, side, playing):
    Thread.__init__(self)

    self.board = board
    self.side = side
    self.playing = playing

  def run(self):
    global mem

    mem['ab_lock'].acquire()

    ab = AlphaBeta(self.side)
    depth = 5
    mem['ab_break'] = False

    while not mem['ab_break']:
      next_move = ab.search(self.board, depth, self.playing, first=True).move
      # best_move = best_move if next_move != -1 else next_move

      if not mem['ab_break']:
        mem['best_move'] = next_move

      # print('depth', depth, 'best_move', mem['best_move'])
      depth += 1

    # temporary
    # next_move = ab.search(self.board, 9, self.playing, first=True).move
    # mem['best_move'] = next_move

    mem['ab_lock'].release()
