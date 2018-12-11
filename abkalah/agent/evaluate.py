import sys

from abkalah import NORTH, SOUTH
from abkalah.game.board import Board

def evaluate(board, player):
  score = 0

  p1_stones = board.count_stones(NORTH)
  p2_stones = board.count_stones(SOUTH)

  score = (board.state[7] - board.state[15]) * 5 + (p1_stones - p2_stones) * 1.5

  if board.state[7] > 49:
    score += 10000
  elif board.state[15] > 49:
    score -= 10000

  mostOpponent = 0
  ai_min = 98
  ai_most = 0

  for i in range(0,7):
    oppositeIndex = 14 - i

    if board.state[i] < ai_min:
      ai_min = board.state[i]

    if board.state[i] > ai_most:
      ai_most = board.state[i]

    if board.state[oppositeIndex] > mostOpponent:
      mostOpponent = board.state[oppositeIndex]

    if board.state[i] == 0:
      canSteal = 0

      if board.state[oppositeIndex] > 0:
        for j in range(0, 7):
          if ((board.state[j] - (i-j)) % 15) == 0 and i != j:
            canSteal = 1

        if canSteal:
            score += board.state[oppositeIndex] * 1.75

    if board.state[oppositeIndex] == 0:
      canOpponentSteal = 0

      if board.state[i] > 0:
          for j in range (8, 15):
            if (board.state[j] - (i-j)) % 15 == 0 and oppositeIndex != j:
              canOpponentSteal = 1

          if canOpponentSteal:
              score -= board.state[i] * 1.75

  if (ai_most - ai_min) > 7:
    score -= ai_most

  ratio = float(p1_stones) / float(p2_stones)

  if ratio < .72:
    score -= mostOpponent * 2

  inverseRatio = float(p2_stones) / float(p1_stones)

  if inverseRatio > .85:
    score -= mostOpponent / 2

  score += board.get_free_turns_for_player(NORTH) * 3
  score -= board.get_free_turns_for_player(SOUTH) * 3

  if player == SOUTH:
    score *= -1

  return score
