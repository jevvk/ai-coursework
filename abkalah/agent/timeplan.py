from abkalah import NORTH, SOUTH
from abkalah.agent.evaluate import evaluate

MIN_DEPTH = 7
MAX_DEPTH = 12
START_GAME_THRESHOLD = 8
MID_GAME_THRESHOLD = 26

def timeplan(board, step, player, depth):
  # 8 - very quick 0.25s
  # 9 - quick 0.9s
  # 10 - slow 0.8s
  # 11 - slowest 5s
  opponent = NORTH if player == SOUTH else SOUTH

  player_well = 7 if player == NORTH else 15
  opp_well = 7 if opponent == NORTH else 15

  # if someone already won, no need to go in depth
  if (board.state[player_well] > 49 or board.state[opp_well] > 49):
    return -1, 5

  ratio = (board.state[player_well] + board.state[opp_well]) / 98

  # our evaluation function plays badly with high depth at the start
  # so less depth is better for now
  if step <= START_GAME_THRESHOLD:
    return -1, 7

  # use fixed depth for more steps
  # this should bring us in a ok position
  if step <= MID_GAME_THRESHOLD:
    return -1, 10

  depth = MIN_DEPTH + ratio * 5
  # if we think we're winning, think for one less level
  depth = depth - 1 if evaluate(board, player) > 0 else depth
  # don't try to reach too deep
  depth = max(depth, 11)

  return -1, depth
