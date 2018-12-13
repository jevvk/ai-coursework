import sys
from threading import Lock

mem = {
  'ab_lock': Lock(),
  'ab_break': False,
  'ab_table': None,
  'ab_depth': 0,
  'ab_max_depth': 20,
  'best_move': 0
}

NORTH = 1
SOUTH = 2
