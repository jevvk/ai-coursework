import sys
import select

from abkalah.interface.interpretor import Interpretor
from abkalah.game.game import Game

interpretor = Interpretor()
game = Game(interpretor)

while True:
  input = select.select([sys.stdin], [], [], 1)[0]

  if input:
    msg = sys.stdin.readline().rstrip()
    move, board = interpretor.receive(msg)

    game.update(move)
    # game.check(board)
  else:
    continue
