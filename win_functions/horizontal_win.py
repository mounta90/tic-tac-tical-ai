import numpy as np


def HorizontalWin(Player, Board):
    # ------------------------------------------
    # Determines if Player has won HORIZONTALLY
    # ------------------------------------------

    board = np.array(Board)

    board_rows = board.shape[0]
    board_columns = board.shape[1]

    # ----------------------------------------
    # Loop through every element of the board;
    # ----------------------------------------
    for row in range(1, board_rows - 1):
        for column in range(1, board_columns - 2):
            # ---------------------------------------------------------------------------------------
            # For each element:
            #   check if the current board position is occupied by Player;
            #   check both horizontal sides for 3 consecutive Player symbols;
            #   if a current board position evaluates to true, return True and exit.
            #   else, False will be returned, if no 3 consecutive horizontal Player symbols are found.
            # ---------------------------------------------------------------------------------------

            # Check if you are looking at the second to last column spot;
            # If you are then dont evaluate it (break out) as you will end up looking outside the board.

            player_check = board[row][column] == Player

            horizontal_check = (
                player_check
                and board[row][column]
                == board[row][column + 1]
                == board[row][column + 2]
            )

            # Return True if the check evaluates to true;
            if horizontal_check:
                return True

            # if horizontal_check:
            #     return (
            #         "horizontal check",
            #         True,
            #         (
            #             (row, column),
            #             (row, column + 1),
            #             (row, column + 2),
            #         ),
            #     )

    # Return False, by default.
    return False
