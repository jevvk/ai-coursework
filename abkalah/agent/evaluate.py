import sys

from abkalah import NORTH, SOUTH
from abkalah.game.board import Board

WIN = 10000
SURE_SEEDS = 15
POSSIBLE_SEEDS = 3.5
CAN_STEAL_SEEDS = 10
OPP_CAN_STEAL_SEEDS = 15
SPREAD_SEEDS = 2.75
SPREAD_SEEDS_THRESHOLD = 8
FREE_TURNS = 6
CLUSTERING_WEIGHT = 1.5
RATIO_THRESHOLD = 0.72
RATIO_WEIGHT = 3
INV_RATIO_THRESHOLD = 0.85
INV_RATIO_WEIGHT = 3

def evaluate(board, player):
  score = 0

  opponent = NORTH if player == SOUTH else SOUTH

  player_stones = board.state[7] if player == NORTH else board.state[15]
  player_total_stones = board.count_stones(player)
  opp_stones = board.state[7] if opponent == NORTH else board.state[15]
  opp_total_stones = board.count_stones(opponent)

  if player_stones > 49:
    score = WIN
  elif opp_stones > 49:
    score = -WIN

  # get stones difference
  score += (player_stones - opp_stones) * SURE_SEEDS + (player_total_stones - player_stones - opp_total_stones + opp_stones) * POSSIBLE_SEEDS

  # get free turns
  score += board.get_free_turns_for_player(player) * FREE_TURNS
  score -= board.get_free_turns_for_player(opponent) * FREE_TURNS

  player_min = 98
  player_most = 0
  opp_most = 0
  clustering = 0

  player_range = range(0, 7) if player == NORTH else range(8, 15)
  opp_range = range(8, 15) if player == NORTH else range(0, 7)

  for index in player_range:
    opp_index = 14 - index
    relative_index = index if player == NORTH else index - 8

    if board.state[index] < player_min:
      player_min = board.state[index]

    if board.state[index] > player_most:
      player_most = board.state[index]

    if board.state[opp_index] > opp_most:
      opp_most = board.state[index]

    # check what we can steal
    if board.state[index] == 0:
      can_steal = False

      if board.state[opp_index] > 0:
        for j in player_range:
          if index != j and ((board.state[j] - (index-j)) % 15) == 0:
            can_steal = True

        if can_steal:
          score += (board.state[opp_index] + 1) * CAN_STEAL_SEEDS

    # check what opponent can steal
    if board.state[opp_index] == 0:
      can_steal = False

      if board.state[index] > 0:
        for j in opp_range:
          if opp_index != j and (board.state[j] - (opp_index-j)) % 15 == 0:
            can_steal = True

        if can_steal:
          score -= (board.state[index] + 1) * OPP_CAN_STEAL_SEEDS

    # cluster stones near our own well
    # the min should give the propper
    clustering += board.state[index] * relative_index

    ratio = float(player_total_stones) / float(opp_total_stones)

  # add clustering score
  score += clustering * CLUSTERING_WEIGHT

  if ratio > RATIO_THRESHOLD:
    score -= opp_most * RATIO_WEIGHT

  inv_ratio = float(opp_total_stones) / float(player_total_stones)

  if inv_ratio > INV_RATIO_THRESHOLD:
    score -= opp_most * INV_RATIO_WEIGHT

  # try not to have bowls that are too big
  if (player_most - player_min) > SPREAD_SEEDS_THRESHOLD:
    score -= player_most * SPREAD_SEEDS

  return score
