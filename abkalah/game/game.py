SOUTH = 1
NORTH = 2
WELLS = 7

class Game:

  from abkalah.game.board import Board

  board = Board()

  def __init__(self, interpretor):
    pass

  def update(self, move, player):

    # receive a move
    # update the board in regards to the move
    # move the balls around
    # check where the last one is
    # if it is on our side, keep the same player
    # if not change player
    opponent = NORTH if player == SOUTH else SOUTH
    beans = self.board[(move * player) - 1]
    current_well = move - 1
    if beans == 0:
      #raise ValueError("Invalid move")

    player_side = player
    self.board[(move * player) - 1] = 0
    current_well += 1


    while True:
      #(((WELLS + 1) * player) - 1)
      if (current_well == (8 * player) - 1) | (current_well == (8 * opponent) - 1):
        # Inside own kalaha
        if player_side == player:
          # Own kalaha - sow
          self.board[(WELLS * player) - 1] += 1
          beans -= 1
          if beans == 0:
            # Turn ended inside own kalaha => new turn for player
            # or victory if no more moves left
            ending = 1
            for position in range(1, WELLS):
              if self.board[current_well - position] > 0:
                ending = 0

            if ending == 1:
              for opp in range(1, (WELLS - 1)):
                if self.board[current_well + opp] > 0:
                  self.board[current_well] += self.board[current_well + opp]
                  self.board[current_well + opp] = 0
            return player

        current_well += 1
        player_side = NORTH if player_side == SOUTH else SOUTH
      else:
        # Inside wells
        beans -= 1
        self.board[current_well] += 1
        if beans == 0:
          # Turn ended
          if player_side == player and self.board[current_well] == 1:
            # Ended in own, empty current well
            opposite_well = 14 - current_well
            self.board[(8 * player) - 1] += (self.board[current_well] + self.board[opposite_well])
            self.board[current_well] = self.board[opposite_well] = 0
          # Game ended - opponent wins?
            ending = 1
            for position in range(1, WELLS):
              if self.board[current_well - position] > 0:
                ending = 0

            if ending == 1:
              for opp in range(0, (WELLS - 1)):
                if self.board[opp] > 0:
                  self.board[(8 * opponent) - 1] += self.board[opp]
                  self.board[opp] = 0
            return opponent
        current_well += 1






