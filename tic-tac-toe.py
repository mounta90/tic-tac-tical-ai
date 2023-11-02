import copy

# -----------------------------------------------------
# import sys

# sys.setrecursionlimit(1000000)
# -----------------------------------------------------

# infinity = 10000
# x = -1
# o = 1


def GetMoves(Board):
    # -------------------------------------------------------------------------
    # Determines all legal moves for Player with current Board,
    # and returns them in MoveList.
    # -------------------------------------------------------------------------

    MoveList = []
    for i in range(0, 3):
        for j in range(0, 3):
            if Board[i][j] == "":
                MoveList.append([i, j])

    return MoveList


def GetHumanMove(Player, Board):
    # -------------------------------------------------------------------------
    # If the opponent is a human, the user is prompted to input a legal move.
    # Determine the set of all legal moves, then check input move against it.
    # -------------------------------------------------------------------------
    MoveList = GetMoves(Board)
    Move = None

    while True:
        Row, Col = map(int, input("Input your move (Row Col): ").split(" "))

        ValidMove = False
        if not ValidMove:
            for move in MoveList:
                if move == [Row, Col]:
                    ValidMove = True
                    Move = move

        if ValidMove:
            break

        print("Invalid move.  ")

    return Move


def ApplyMove(Board, Move, Player):
    # -------------------------------------------------------------------------
    # Perform the given move, and update Board.
    # -------------------------------------------------------------------------

    Row, Col = Move
    # newBoard = copy.deepcopy(Board)
    Board[Row][Col] = Player
    return Board


def SimulateMove(Board, Move, Player):
    # ------------------------------------------------------------------------------------
    # Simulate the given move on a copy, and DONT update game Board, only update the copy.
    # This function is used for the Minimax algorithm.
    # ------------------------------------------------------------------------------------

    Row, Col = Move
    newBoard = copy.deepcopy(Board)
    newBoard[Row][Col] = Player
    return newBoard


def InitBoard():
    # -------------------------------------------------------------------------
    # Initialize the game board.
    # -------------------------------------------------------------------------

    Board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
    ]

    return Board


def ShowBoard(Board):
    print("")
    row_divider = "+" + "-" * (3 * 4 - 1) + "+"
    print(row_divider)

    for i in range(0, 3):
        for j in range(0, 3):
            if Board[i][j] == x:
                print("| X ", end="")
            elif Board[i][j] == o:
                print("| O ", end="")
            elif Board[i][j] == "":
                print("|   ", end="")
        print("|")
        print(row_divider)

    print("")


def HorizontalWin(Player, Board):
    for row in range(0, 3):
        if Board[row][0] == Player and Board[row][0] == Board[row][1] == Board[row][2]:
            return True

    return False


def VerticalWin(Player, Board):
    for column in range(0, 3):
        if (
            Board[0][column] == Player
            and Board[0][column] == Board[1][column] == Board[2][column]
        ):
            return True

    return False


def DiagonalWin(Player, Board):
    first_check = Board[0][0] == Player and Board[0][0] == Board[1][1] == Board[2][2]
    second_check = Board[0][2] == Player and Board[0][2] == Board[1][1] == Board[2][0]

    return first_check or second_check


def Win(Player, Board):
    # -------------------------------------------------------------------------
    # Determines if Player has won, by finding '3 in a row'.
    # -------------------------------------------------------------------------

    return (
        HorizontalWin(Player, Board)
        or VerticalWin(Player, Board)
        or DiagonalWin(Player, Board)
    )


def Tie(Board):
    full_count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if Board[i][j] != "":
                full_count += 1

    if full_count == 9:
        return True
    else:
        return False


def Minimax(Player, Board):
    # -------------------------------------------------------------------------
    # Minimax Base Case: One of the players wins.
    # If a player wins, return their corresponding score:
    # x : -1
    # o : 1
    # -------------------------------------------------------------------------

    o_wins = Win(o, Board)
    x_wins = Win(x, Board)
    is_there_a_tie = Tie(Board)

    if o_wins:
        return o
    elif x_wins:
        return x
    elif is_there_a_tie:
        return 0
    else:
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # Given a board state, go through all possible moves, and apply them;
        # Apply the Minimax algorithm on that state;
        # For all the state values, return the max or min, depending on the player.
        # -------------------------------------------------------------------------
        MoveList = GetMoves(Board)

        if Player == o:
            best_value = -infinity
            for move in MoveList:
                board = SimulateMove(Board, move, Player)
                move_value = Minimax(x, board)

                best_value = max(best_value, move_value)

            return best_value

        else:
            best_value = infinity
            for move in MoveList:
                board = SimulateMove(Board, move, Player)
                move_value = Minimax(o, board)

                best_value = min(best_value, move_value)

            return best_value


def GetComputerMove(Player, Board):
    # -------------------------------------------------------------------------
    # If the opponent is a computer, use artificial intelligence to select
    # the best move.
    # For this demo, a move is chosen at random from the list of legal moves.
    # You need to write your own code to get the best computer move.
    # -------------------------------------------------------------------------

    # ------------------------------------
    # ORIGINAL CODE
    # # ------------------------------------
    # MoveList = GetMoves(Player, Board)
    # k = randrange(0, len(MoveList))
    # Move = MoveList[k]
    # ------------------------------------

    # ----------------------------------------------------
    # Get all possible moves for the current board state.
    # ----------------------------------------------------
    MoveList = GetMoves(Board)

    # ------------------------------------------------------------------------------------------------------------
    # Check which symbol the computer is;
    # If it is an 'o', it is the maximizing player;
    # If it is an 'x', it is the minimizing player.
    # ------------------------------------------------------------------------------------------------------------
    # At the beginning, the best move is not known;
    # Thus, go through all possible moves;
    # Simulate them;
    # Get their minimax values;
    # If their minimax values are less than or greater than, depending on the player, update best value and move;
    # Once all the moves have been seen, return the best move;
    # ------------------------------------------------------------------------------------------------------------
    if Player == o:
        best_value = -infinity
        best_move = None
        for move in MoveList:
            board = SimulateMove(Board, move, Player)
            move_value = Minimax(x, board)

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move

    else:
        best_value = infinity
        best_move = None
        for move in MoveList:
            board = SimulateMove(Board, move, Player)
            move_value = Minimax(o, board)

            if move_value < best_value:
                best_value = move_value
                best_move = move

        return best_move


if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # A move is represented by a list of 4 elements, representing 2 pairs of
    # coordinates, (FromRow, FromCol) and (ToRow, ToCol), which represent the
    # positions of the piece to be moved, before and after the move.
    # -------------------------------------------------------------------------
    x = -1
    o = 1
    infinity = 10000  # Value of a winning board

    Board = InitBoard()
    ShowBoard(Board)
    moves = GetMoves(Board)

    print(moves)

    for n in range(5):
        Move = GetHumanMove(x, Board)
        Board = ApplyMove(Board, Move, x)
        ShowBoard(Board)
        Move = GetComputerMove(o, Board)
        Board = ApplyMove(Board, Move, o)
        ShowBoard(Board)
