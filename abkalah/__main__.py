import sys
import select

from abkalah.interface.interpretor import Interpretor
from abkalah.game.game import Game

game = Game()
interpretor = Interpretor(game)

while True:
  input = select.select([sys.stdin], [], [], 1)[0]

  if input:
    msg = sys.stdin.readline().rstrip()
    interpretor.receive(msg)
  else:
    continue
