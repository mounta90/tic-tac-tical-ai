import numpy as np


def DiagonalWin(Player, Board):
    # ------------------------------------------
    # Determines if Player has won DIAGONALLY
    # ------------------------------------------

    board = np.array(Board)

    board_rows = board.shape[0]
    board_columns = board.shape[1]

    # ----------------------------------------
    # Loop through every element of the board;
    # ----------------------------------------
    for row in range(1, board_rows - 2):
        for column in range(1, board_columns - 2):
            # ---------------------------------------------------------------------------------------
            # For each element:
            #   check if the current board position is occupied by Player;
            #   check all 4 diagonal configurations for 3 consecutive Player symbols;
            #   if a current board position evaluates to true, return True and exit.
            #   else, False will be returned, if no 3 consecutive diagonal Player symbols are found.
            # ---------------------------------------------------------------------------------------

            player_check = board[row][column] == Player

            south_west_check = (
                player_check
                and board[row][column]
                == board[row + 1][column - 1]
                == board[row + 2][column - 2]
            )
            south_east_check = (
                player_check
                and board[row][column]
                == board[row + 1][column + 1]
                == board[row + 2][column + 2]
            )

            # Return True if:
            # player_check AND south_west_check OR south_east_check
            # evaluate to true.

            if player_check and south_west_check or south_east_check:
                return True

            # if north_west_check:
            #     return (
            #         "north west check",
            #         True,
            #         (
            #             (row, column),
            #             (row - 1, column - 1),
            #             (row - 2, column - 2),
            #         ),
            #     )
            # elif north_east_check:
            #     return (
            #         "north east check",
            #         True,
            #         (
            #             (row, column),
            #             (row - 1, column + 1),
            #             (row - 2, column + 2),
            #         ),
            #     )
            # elif south_west_check:
            #     return (
            #         "south west check",
            #         True,
            #         (
            #             (row, column),
            #             (row + 1, column - 1),
            #             (row + 2, column - 2),
            #         ),
            #     )
            # elif south_east_check:
            #     return (
            #         "south east check",
            #         True,
            #         (
            #             (row, column),
            #             (row + 1, column + 1),
            #             (row + 2, column + 2),
            #         ),
            #     )

    # Return False, by default.
    return False
