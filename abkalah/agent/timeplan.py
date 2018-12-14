from abkalah.agent.evaluate import evaluate
# TODO: return the number of seconds (float) to spend at a given time
# note: arguments don't necessarily have to be these
def timeplan(board, step, side, depth):
    # return 1, -1
    # player_stones = board.state[15] if side == NORTH else board.state[7]
    # opponent_stones = board.state[7] if side == NORTH else board.state[15]
    score = evaluate(board, side)
    # player_stones_percentage = 1 - float(opponent_stones) / float(player_stones)

    # if player_stones_percentage > 0.75:
    #     return 0, 3
    # elif player_stones_percentage > 0.5:
    #     return 0, 5
    # elif player_stones_percentage > 0.25:
    #     return 0, 7
    if score <= 0:
        return 3, -1
    else:
        return 1, depth + 7
