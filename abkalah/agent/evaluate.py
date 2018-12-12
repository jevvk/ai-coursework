import sys

from abkalah import NORTH, SOUTH
from abkalah.game.board import Board

WIN = 10000
SURE_SEEDS = 5
POSSIBLE_SEEDS = 1.25
CAN_STEAL_SEEDS = 5
OPP_CAN_STEAL_SEEDS = 5
SPREAD_SEEDS = 1.25
SPREAD_SEEDS_THRESHOLD = 7
FREE_TURNS = 4

def evaluate(board, player):
  score = 0

  p1_stones = board.count_stones(NORTH)
  p2_stones = board.count_stones(SOUTH)

  score = (board.state[7] - board.state[15]) * SURE_SEEDS + (p1_stones - p2_stones) * POSSIBLE_SEEDS

  if board.state[7] > 49:
    score += WIN
  elif board.state[15] > 49:
    score -= WIN

  mostOpponent = 0
  ai_min = 98
  ai_most = 0

  for i in range(0, 7):
    oppositeIndex = 14 - i

    if board.state[i] < ai_min:
      ai_min = board.state[i]

    if board.state[i] > ai_most:
      ai_most = board.state[i]

    if board.state[oppositeIndex] > mostOpponent:
      mostOpponent = board.state[oppositeIndex]

    if board.state[i] == 0:
      canSteal = False

      if board.state[oppositeIndex] > 0:
        for j in range(0, 7):
          if i != j and ((board.state[j] - (i-j)) % 15) == 0:
            canSteal = True

        if canSteal:
          score += board.state[oppositeIndex] * CAN_STEAL_SEEDS

    if board.state[oppositeIndex] == 0:
      canOpponentSteal = False

      if board.state[i] > 0:
          for j in range (8, 15):
            if oppositeIndex != j and (board.state[j] - (oppositeIndex-j)) % 15 == 0:
              canOpponentSteal = True

          if canOpponentSteal:
            score -= board.state[i] * OPP_CAN_STEAL_SEEDS

  if (ai_most - ai_min) > SPREAD_SEEDS_THRESHOLD:
    score -= ai_most * SPREAD_SEEDS

  ratio = float(p1_stones) / float(p2_stones)

  if ratio < .72:
    score -= mostOpponent * 2

  inverseRatio = float(p2_stones) / float(p1_stones)

  if inverseRatio > .85:
    score -= mostOpponent / 2

  score += board.get_free_turns_for_player(NORTH) * FREE_TURNS
  score -= board.get_free_turns_for_player(SOUTH) * FREE_TURNS

  if player == SOUTH:
    score *= -1

  return score
