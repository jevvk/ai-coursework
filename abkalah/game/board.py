from abkalah import NORTH, SOUTH

class Board:
  def __init__(self, board = [7] * 7 + [0] + [7] * 7 + [0]):
    self.state = board

  def move(self, move, first_turn = False):
    moved_board = [ i for i in self.state ]

    player = NORTH if move < 7 else SOUTH
    opponent = NORTH if player == SOUTH else SOUTH

    next_player = opponent

    stones = moved_board[move]
    moved_board[move] = 0

    # game end check
    if not self.has_moves(player):
      if player == NORTH:
        for i in range(8, 15):
          moved_board[15] += moved_board[i]
          moved_board[i] = 0
      else:
        for i in range(0, 7):
          moved_board[7] += moved_board[i]
          moved_board[i] = 0
      
      return Board(moved_board), opponent

    while stones > 0:
      # update next move
      move = (move + 1) % 16

      # don't add to opponent's well
      if player == NORTH and move == 15:
        move = 0
      elif player == SOUTH and move == 7:
        move = 8
      
      moved_board[move] += 1
      stones -= 1
  
    # check if the previous bowl was empty and capture opponent's
    if moved_board[move] == 1:
      opposite_well = 14 - move

      if player == NORTH and move < 7 and moved_board[opposite_well] > 0:
        moved_board[7] += moved_board[opposite_well] + 1
        moved_board[opposite_well] = 0
        moved_board[move] = 0
      elif player == SOUTH and move > 7 and move != 15 and moved_board[opposite_well] > 0:
        moved_board[15] += moved_board[opposite_well] + 1
        moved_board[opposite_well] = 0
        moved_board[move] = 0

    # check if stone was placed inside the player's own well
    if not first_turn and ((player == NORTH and move == 7) or (player == SOUTH and move == 15)):
      next_player = player
    
    return Board(moved_board), next_player

  def has_moves(self, player):
    if player == NORTH:
      for i in range(0,7):
        if self.state[i] > 0:
          return True
    else:
      for i in range(8, 15):
        if self.state[i] > 0:
          return True

    return False

  def available_moves(self, player):
    moves = []

    if player == NORTH:
      for i in range(0,7):
        if self.state[i] > 0:
          moves.append(i)
    else:
      for i in range(8, 15):
        if self.state[i] > 0:
          moves.append(i)

    return moves
  
  def is_end(self, player):
    if player == NORTH:
      for i in range(0, 7):
        if self.state[i] > 0: return False

    else:
      for i in range(8, 15):
        if self.state[i] > 0: return False

    return True

  def count_stones(self, player):
    sum = 0

    if player == NORTH:
      for i in range(0, 8):
        sum += self.state[i]
    else:
      for i in range(8, 16):
        sum += self.state[i]

    return sum

  def get_free_turns_for_player(self, player):
    count = 0

    if player == NORTH:
      for i in range(0, 7):
        if self.state[i] == (7 - i):
          count += 1
    else:
      for i in range(8, 15):
        if self.state[i] == (15 - i):
          count += 1

    return count
  
  def __str__(self):
    return str([ self.state[0:7], self.state[7], self.state[8:15], self.state[15] ])
