import numpy as np


def VerticalWin(Player, Board):
    # ------------------------------------------
    # Determines if Player has won VERTICALLY
    # ------------------------------------------

    board = np.array(Board)

    board_rows = board.shape[0]
    board_columns = board.shape[1]

    # ----------------------------------------
    # Loop through every element of the board;
    # ----------------------------------------
    for row in range(1, board_rows - 2):
        for column in range(1, board_columns - 1):
            # ---------------------------------------------------------------------------------------
            # For each element:
            #   check if the current board position is occupied by Player;
            #   check both vertical sides for 3 consecutive Player symbols;
            #   if a current board position evaluates to true, return True and exit.
            #   else, False will be returned, if no 3 consecutive vertical Player symbols are found.
            # ---------------------------------------------------------------------------------------

            player_check = board[row][column] == Player

            vertical_check = (
                player_check
                and board[row][column]
                == board[row + 1][column]
                == board[row + 2][column]
            )

            # Return True if vertical_check evaluates to true;
            if vertical_check:
                return True

            # if vertical_check:
            #     return (
            #         "vertical check",
            #         True,
            #         (
            #             (row, column),
            #             (row + 1, column),
            #             (row + 2, column),
            #         ),
            #     )

    # Return False, by default.
    return False
