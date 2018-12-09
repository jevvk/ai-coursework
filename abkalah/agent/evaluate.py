import sys
def eval(Board board):
    score = 0
    p1_stones = board.count_stones(1)
    p2_stones = board.count_stones(2)

    score = (board.state[7] - board.state[15]) + (p1_stones - p2_stones)

    if board.state[7] > 49:
        score += 1000
    elif board.state[15] > 49:
        score -= 1000

    countEmpty = 0
    mostOpponent = 0
    ai_min = sys.maxint
    ai_most = -sys.maxint - 1
    for i in range(0,7):
        oppositeIndex = 14 - i
        if board.state[i] < ai_min:
            ai_min = board.state[i]

        if board.state[i] > ai_most:
            ai_most = board.state[i]

        if board.state[i] == 0:
            if board.state[oppositeIndex] > 0:
                canSteal = 0
                for j in range(0,7):
                    if ((board.state[j] - (i-j)) % 15) == 0:
                        canSteal = 1
                if canSteal:
                    score += state[oppositeIndex]
            countEmpty+=1

        if board.state[oppositeIndex] > mostOpponent:
            mostOpponent = board.state[oppositeIndex]

        if board.state[oppositeIndex] == 0:
            canOpponentSteal = 0
            if board.state[oppositeIndex] > 6: # WTF is this for?
                for j in range (8, 15):
                    if (board.state[j] - (i-j)) % 15 == 0:
                        canOpponentSteal = 1
                if canOpponentSteal:
                    score -= board.state[i]

    if (ai_most - ai_min) > 10:
        score -= 1

    ratio = float(p1_stones) / float(p2_stones)
    if ration > .72:
        score -= mostOpponent * 2

    inverseRation = float(p2_stones) / float(p1_stones)
    if inverseRatio > .85:
        score -= mostOpponent / 2

    score += board.get_free_turns_for_player(1)
    score -= board.get_free_turns_for_player(2)

    if player_num == 2:
        score *= -1

    return score
