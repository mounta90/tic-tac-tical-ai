from code_hw4 import Empty, NumCols, NumRows


def ntasnim_h(Player, Board):
    player_score = 0
    opponent_score = 0

    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            if Board[i][j] == Player:
                player_score += 1
            elif Board[i][j] != Empty:
                opponent_score += 1

    return player_score - opponent_score
