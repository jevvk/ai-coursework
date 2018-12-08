from abkalah.game.board import Board
# Do we pass the board as an array or as an Board object
# How do we remember each player's number? TODO: Replace Player.You, Player.Opp
# How do we make a difference between a normal move and a SWAP? line36
class Interpretor:
  def __init__(self):
    pass

  # Messages can be of 3 types: START, CHANGE, END
  #
  # START marks the beginning of the game. "START;North" means you are P2
  # A CHANGE is either a SWAP or a MOVE
  # END marks the end of the game
  #
  # return player, move, board
  def receive(self, message):
    if message[:5] == 'START':
        if message[6:] == 'South':
            return 1, None, Board.INITIAL_STATE
        else:
            return 2, None, Board.INITIAL_STATE
    elif message[:6] == 'CHANGE':
        if message[7:11] == 'SWAP':
            boardArray = message[12:-4].split(",")
            return 'OPP', None, boardArray
        else:
            player = message[-3:] # YOU / OPP
            move = message[7]
            boardArray = message[9:32].split(",")
            return player, move, boardArray
    else:
        return None, None, None


  # send move to stdout
  def send(self, board, move):
    if move == 'SWAP':
        sys.stdout.write('SWAP\n')
    else:
        sys.stdout.write(move + '\n')
    sys.stdout.flush()
    
