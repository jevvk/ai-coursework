import sys
from threading import Lock

mem = {
  'ab_lock': Lock(),
  'ab_break': False,
  'best_move': 0
}

NORTH = 1
SOUTH = 2
