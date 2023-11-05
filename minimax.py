from code_hw4 import GetMoves, MaxDepth, SimulateMove, Win
from heuristic_function import ntasnim_h


def Minimax(Player, Board, Depth, Alpha, Beta):
    # -------------------------------------------------------------------------
    # Minimax Base Case: One of the players wins.
    # If a player wins, return their corresponding score:
    # x : -1
    # o : 1
    # -------------------------------------------------------------------------

    o = 1
    x = -1
    infinity = 10000

    o_wins = Win(o, Board)
    x_wins = Win(x, Board)

    global max_depth

    if Depth == 0:
        max_depth = MaxDepth - Depth
        return ntasnim_h(Player, Board)
    if o_wins:
        max_depth = MaxDepth - Depth
        return o
    elif x_wins:
        max_depth = MaxDepth - Depth
        return x
    else:
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # Given a board state, go through all possible moves, and apply them;
        # Apply the Minimax algorithm on that state;
        # In addition, use Alpha-Beta Pruning.
        # For all the state values, return the max or min, depending on the player.
        # -------------------------------------------------------------------------
        MoveList = GetMoves(Player, Board)

        global states_evaluated

        if Player == o:
            best_value = -infinity
            for move in MoveList:
                board = SimulateMove(Board, Move=move)

                states_evaluated += 1

                move_value = Minimax(
                    Player=x,
                    Board=board,
                    Alpha=Alpha,
                    Beta=Beta,
                    Depth=Depth - 1,
                )

                best_value = max(best_value, move_value)

                Alpha = max(Alpha, move_value)

                if Beta <= Alpha:
                    break

            return best_value

        else:
            best_value = infinity
            for move in MoveList:
                board = SimulateMove(Board, Move=move)
                states_evaluated += 1

                move_value = Minimax(
                    Player=o,
                    Board=board,
                    Alpha=Alpha,
                    Beta=Beta,
                    Depth=Depth - 1,
                )

                best_value = min(best_value, move_value)

                Beta = min(Beta, move_value)

                if Beta <= Alpha:
                    break

            return best_value
