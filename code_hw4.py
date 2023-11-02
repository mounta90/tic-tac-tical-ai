"""
COSC 4550-COSC5550 - Introduction to AI - Homework 4
"""
# -------------------------------------------------------------------------
# Tac-Tac-Tical
# This program is designed to play Tic-Tac-Tical, using lookahead and board heuristics.
# It will allow the user to play a game against the machine, or allow the machine
# to play against itself for purposes of learning to improve its play.  All 'learning'
# code has been removed from this program.
#
# Tic-Tac-Tical is a 2-player game played on a grid. Each player has the same number
# of tokens distributed on the grid in an initial configuration.  On each turn, a player
# may move one of his/her tokens one unit either horizontally or vertically (not
# diagonally) into an unoccupied square.  The objective is to be the first player to get
# three tokens in a row, either horizontally, vertically, or diagonally.
#
# The board is represented by a matrix with extra rows and columns forming a
# boundary to the playing grid. Squares in the playing grid can be occupied by
# either 'X', 'O', or 'Empty' spaces.  The extra elements are filled with 'Out of Bounds'
# squares, which makes some of the computations simpler.
# -------------------------------------------------------------------------

from __future__ import print_function
import random
from random import randrange
import copy

# -----------------------------------------------------
# MY IMPORTS
# -----------------------------------------------------
# win functions
# -----------------------------------------------------
from win_functions.horizontal_win import HorizontalWin
from win_functions.vertical_win import VerticalWin
from win_functions.diagonal_win import DiagonalWin

# -----------------------------------------------------

# -----------------------------------------------------
# import sys

# sys.setrecursionlimit(1000000)
# -----------------------------------------------------


def GetMoves(Player, Board):
    # -------------------------------------------------------------------------
    # Determines all legal moves for Player with current Board,
    # and returns them in MoveList.
    # -------------------------------------------------------------------------

    MoveList = []
    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            if Board[i][j] == Player:
                # -------------------------------------------------------------
                #  Check move directions (m,n) = (-1,0), (0,-1), (0,1), (1,0)
                # -------------------------------------------------------------
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        if abs(m) != abs(n):
                            if Board[i + m][j + n] == Empty:
                                MoveList.append([i, j, i + m, j + n])

    return MoveList


def GetHumanMove(Player, Board):
    # -------------------------------------------------------------------------
    # If the opponent is a human, the user is prompted to input a legal move.
    # Determine the set of all legal moves, then check input move against it.
    # -------------------------------------------------------------------------
    MoveList = GetMoves(Player, Board)
    Move = None

    while True:
        FromRow, FromCol, ToRow, ToCol = map(
            int, input("Input your move (FromRow, FromCol, ToRow, ToCol): ").split(" ")
        )

        ValidMove = False
        if not ValidMove:
            for move in MoveList:
                if move == [FromRow, FromCol, ToRow, ToCol]:
                    ValidMove = True
                    Move = move

        if ValidMove:
            break

        print("Invalid move.  ")

    return Move


def ApplyMove(Board, Move):
    # -------------------------------------------------------------------------
    # Perform the given move, and update Board.
    # -------------------------------------------------------------------------

    FromRow, FromCol, ToRow, ToCol = Move
    # newBoard = copy.deepcopy(Board)
    Board[ToRow][ToCol] = Board[FromRow][FromCol]
    Board[FromRow][FromCol] = Empty
    return Board


# def ReapplyMove(Board, Move):
#     # ------------------------------------------------------------------------------------
#     # Returns the board to its original state, after applying a move.
#     # This function is used for the Minimax algorithm.
#     # ------------------------------------------------------------------------------------

#     ToRow, ToCol, FromRow, FromCol = Move
#     # newBoard = copy.deepcopy(Board)
#     Board[FromRow][FromCol] = Board[ToRow][ToCol]
#     Board[ToRow][ToCol] = Empty
#     return Board


def SimulateMove(Board, Move):
    # ------------------------------------------------------------------------------------
    # Simulate the given move on a copy, and DONT update game Board, only update the copy.
    # This function is used for the Minimax algorithm.
    # ------------------------------------------------------------------------------------

    FromRow, FromCol, ToRow, ToCol = Move
    newBoard = copy.deepcopy(Board)
    newBoard[ToRow][ToCol] = newBoard[FromRow][FromCol]
    newBoard[FromRow][FromCol] = Empty
    return newBoard


def InitBoard(Board):
    # -------------------------------------------------------------------------
    # Initialize the game board.
    # -------------------------------------------------------------------------

    for i in range(0, BoardRows + 1):
        for j in range(0, BoardCols + 1):
            Board[i][j] = OutOfBounds

    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            Board[i][j] = Empty

    # Board[1][1] = x
    # Board[2][1] = x
    # Board[4][1] = x

    # Board[2][2] = o
    # Board[3][3] = o
    # Board[4][3] = o

    for j in range(1, NumCols + 1):
        if odd(j):
            Board[1][j] = x
            Board[NumRows][j] = o
        else:
            Board[1][j] = o
            Board[NumRows][j] = x


def odd(n):
    return n % 2 == 1


def ShowBoard(Board):
    print("")
    row_divider = "+" + "-" * (NumCols * 4 - 1) + "+"
    print(row_divider)

    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            if Board[i][j] == x:
                print("| X ", end="")
            elif Board[i][j] == o:
                print("| O ", end="")
            elif Board[i][j] == Empty:
                print("|   ", end="")
        print("|")
        print(row_divider)

    print("")


def Win(Player, Board):
    # -------------------------------------------------------------------------
    # Determines if Player has won, by finding '3 in a row'.
    # -------------------------------------------------------------------------

    return (
        HorizontalWin(Player, Board)
        or VerticalWin(Player, Board)
        or DiagonalWin(Player, Board)
    )


def Minimax(Player, Board):
    # -------------------------------------------------------------------------
    # Minimax Base Case: One of the players wins.
    # If a player wins, return their corresponding score:
    # x : -1
    # o : 1
    # -------------------------------------------------------------------------

    o_wins = Win(o, Board)
    x_wins = Win(x, Board)

    if o_wins:
        return o
    elif x_wins:
        return x
    else:
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # Given a board state, go through all possible moves, and apply them;
        # Apply the Minimax algorithm on that state;
        # For all the state values, return the max or min, depending on the player.
        # -------------------------------------------------------------------------
        MoveList = GetMoves(Player, Board)

        if Player == o:
            best_value = -infinity
            for move in MoveList:
                board = SimulateMove(Board, Move=move)
                move_value = Minimax(Player=x, Board=board)

                best_value = max(best_value, move_value)

            return best_value

        else:
            best_value = infinity
            for move in MoveList:
                board = SimulateMove(Board, Move=move)
                move_value = Minimax(Player=o, Board=board)

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
    MoveList = GetMoves(Player, Board)

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
            board = SimulateMove(Board, Move=move)
            move_value = Minimax(Player=x, Board=board)

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move

    else:
        best_value = infinity
        best_move = None
        for move in MoveList:
            board = SimulateMove(Board, Move=move)
            move_value = Minimax(Player=o, Board=board)

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
    Empty = 0
    OutOfBounds = 2
    NumRows = 5
    BoardRows = NumRows + 1
    NumCols = 4
    BoardCols = NumCols + 1
    MaxMoves = 4 * NumCols
    NumInPackedBoard = 4 * (BoardRows + 1) * (BoardCols + 1)
    infinity = 10000  # Value of a winning board
    MaxDepth = 4
    Board = [[0 for col in range(BoardCols + 1)] for row in range(BoardRows + 1)]

    print("\nThe squares of the board are numbered by row and column, with '1 1' ")
    print("in the upper left corner, '1 2' directly to the right of '1 1', etc.")
    print("")
    print("Moves are of the form 'i j m n', where (i,j) is a square occupied")
    print("by your piece, and (m,n) is the square to which you move it.")
    print("")
    print("You move the 'X' pieces.\n")

    InitBoard(Board)
    ShowBoard(Board)

    MoveList = GetMoves(x, Board)
    print(MoveList)
    MoveList = GetMoves(o, Board)
    print(MoveList)

    for n in range(5):
        Move = GetHumanMove(x, Board)
        Board = ApplyMove(Board, Move)
        ShowBoard(Board)
        Move = GetComputerMove(o, Board)
        Board = ApplyMove(Board, Move)
        ShowBoard(Board)
