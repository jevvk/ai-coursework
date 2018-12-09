WELLS = 7
from abkalah import NORTH, SOUTH

class Board:
  def __init__(self, board = [7] * 7 + [0] + [7] * 7 + [0]):
    self.state = board

  def move(self, move):
    # receive a move
    # update the board in regards to the move
    # move the balls around
    # check where the last one is
    # if it is on our side, keep the same player
    # if not change player

    #inherit values from previous board
    moved_board = [ i for i in self.board ]

    opponent = NORTH if move < 8 else SOUTH
    player = NORTH if opponent == SOUTH else SOUTH

    beans = moved_board[move]
    current_well = move

    moved_board[move] = 0
    current_well += 1
    player_side = player

    while beans > - 1:
      if (current_well == (8 * player) - 1) | (current_well == (8 * opponent) - 1):
      # Inside own kalaha
        if player_side == player:
        # Own kalaha - sow
          moved_board[current_well] += 1
          beans -= 1
          if beans == 0:
          # Turn ended inside own kalaha => new turn for player
          # or victory if no more moves left
            ending = 1
            for position in range(1, WELLS):
              if moved_board[current_well - position] > 0:
                ending = 0

            if ending == 1:
              for opp in range(1, WELLS):
                if moved_board[current_well + opp] > 0:
                  moved_board[current_well] += moved_board[current_well + opp]
                  moved_board[current_well + opp] = 0
            return Board(moved_board), player
          current_well += 1
        else :
          current_well = 0;
          
        player_side = NORTH if player_side == SOUTH else SOUTH
      else:
      # Inside wells
        beans -= 1
        moved_board[current_well] += 1
        if beans == 0:
        # Turn ended
          if player_side == player and moved_board[current_well] == 1:
            # Ended in own, empty current well
            opposite_well = 14 - current_well
            moved_board[(8 * player) - 1] += (moved_board[current_well] + moved_board[opposite_well])
            moved_board[current_well] = moved_board[opposite_well] = 0
          # Game ended - opponent wins?
            ending = 1
            for position in range(1, WELLS):
              if moved_board[((8 * player) - 1) - position] > 0:
                ending = 0

            if ending == 1:
              for opp in range(0, (WELLS - 1)):
                if moved_board[opp] > 0:
                  moved_board[(8 * opponent) - 1] += moved_board[opp]
                  moved_board[opp] = 0
            return Board(moved_board), opponent
        current_well += 1

  def available_moves(self, player):
    pass

  def count_stones(self, player_num):
    sum = 0
    if player_num == 1:
        for i in range(0,7):
            sum += self.state[i]
    else:
        for i in range(8, 15):
            sum += self.state[i]
    return sum

  def get_free_turns_for_player(self, player_num):
    count = 0
    if player_num == 1:
      for i in range(0,7):
          if self.state[i] == (7-i):
              count += 1
    else:
      for i in range(8, 15):
          if self.state[i] == (15-i):
              count += 1
    return count
