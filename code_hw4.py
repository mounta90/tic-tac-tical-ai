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
import math
import random
from random import randrange
import copy
import timeit
import numpy as np


states_evaluated = 0
max_depth = 0


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

    # Return False, by default.
    return False


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

    # Return False, by default.
    return False


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

    # Return False, by default.
    return False


def Win(Player, Board):
    # -------------------------------------------------------------------------
    # Determines if Player has won, by finding '3 in a row'.
    # -------------------------------------------------------------------------

    return (
        HorizontalWin(Player, Board)
        or VerticalWin(Player, Board)
        or DiagonalWin(Player, Board)
    )


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
    global time_of_stop

    if Depth == 0:
        max_depth = MaxDepth - Depth
        return W10247393_h(Player=Player, Board=Board)
    elif o_wins:
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

                # Alpha = max(Alpha, move_value)

                # if Beta <= Alpha:
                #     break

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

                # Beta = min(Beta, move_value)

                # if Beta <= Alpha:
                #     break

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

    global states_evaluated

    if Player == o:
        best_move = None

        best_value = -infinity
        for move in MoveList:
            board = SimulateMove(Board, Move=move)

            states_evaluated += 1

            move_value = Minimax(
                Player=x,
                Board=board,
                Alpha=-infinity,
                Beta=infinity,
                Depth=MaxDepth,
            )

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move

    else:
        best_move = None
        best_value = infinity
        for move in MoveList:
            board = SimulateMove(Board, Move=move)

            states_evaluated += 1

            move_value = Minimax(
                Player=o,
                Board=board,
                Alpha=-infinity,
                Beta=infinity,
                Depth=MaxDepth,
            )

            if move_value < best_value:
                best_value = move_value
                best_move = move

        return best_move


def W10247393_h(Player, Board):
    player_position_rows = []
    player_position_columns = []

    for row in range(0, BoardRows):
        for column in range(0, BoardCols):
            if Board[row][column] == Player:
                player_position_rows.append(float(row))
                player_position_columns.append(float(column))

    player_rows_max = max(player_position_rows)
    player_rows_min = min(player_position_rows)

    player_columns_max = max(player_position_columns)
    player_columns_min = min(player_position_columns)

    player_rows_difference = player_rows_max - player_rows_min
    player_columns_difference = player_columns_max - player_columns_min

    if player_rows_difference == 0:
        heuristic_value = (1 / 0.0001) + (1 / player_columns_difference)
    elif player_columns_difference == 0:
        heuristic_value = (1 / player_rows_difference) + (1 / 0.0001)
    elif player_rows_difference == 0 and player_columns_difference == 0:
        heuristic_value = (1 / 0.0001) + (1 / 0.0001)
    else:
        heuristic_value = (1 / player_rows_difference) + (1 / player_columns_difference)

    return heuristic_value


# # This TreeNode class is used to implement the heuristic.
# class TreeNode:
#     def __init__(self, Board, ParentNode=None):
#         # initialize the current board state:
#         self.board = Board

#         # check if this node (state) is terminal:
#         if Win(Player=o, Board=self.board) or Win(Player=x, Board=self.board):
#             self.is_terminal = True
#         else:
#             self.is_terminal = False

#         self.is_expanded = self.is_terminal

#         # assign a parent node if there exists one:
#         self.parent_node = ParentNode

#         # initialize the MCTS node's data:
#         self.simulations = 0
#         self.wins = 0

#         # initialize the MCTS node's children:
#         self.children = []


# # The heuristic function which uses a Monte Carlo Tree Search to get a heuristic value for a board position.
# def MonteCarloHeuristic(CurrentBoard, CurrentPlayer):
#     # Allow current board to be root node:
#     root_node = TreeNode(
#         Board=CurrentBoard,
#         ParentNode=None,
#     )

#     # Allow MCTS to have x iterations:
#     for i in range(2):
#         # 1. SELECT
#         node = Select(
#             Node=root_node,
#             Player=CurrentPlayer,
#         )

#         # 2. SIMULATE and return a 1 for a win, or a 0 for a loss.
#         win = Rollout(
#             Board=node.board,
#             Player=CurrentPlayer,
#         )

#         print(win)

#         # 3. BACKPROPOGATE the result up the tree.
#         BackPropogate(
#             Node=node,
#             Win=win,
#         )

#     # This is the heuristic value:
#     return root_node.wins / root_node.simulations


# # Use a selection policy to choose the most promising node.
# def GetBestNode(Node):
#     best_node = None
#     best_ucb1 = -infinity

#     for child_node in Node.children:
#         child_ucb1 = UCB1(ChildNode=child_node, ParentNode=Node)

#         if child_ucb1 > best_ucb1:
#             best_ucb1 = child_ucb1
#             best_node = child_node

#     return best_node


# # Randomly simulate the game until you hit a terminal Win state.
# def Rollout(Player, Board):
#     if Player == o and Win(o, Board):
#         return 1.0
#     elif Player == o and Win(x, Board):
#         return 0.0
#     elif Player == x and Win(x, Board):
#         return 1.0
#     elif Player == x and Win(o, Board):
#         return 0.0
#     else:
#         if Player == o:
#             MoveList = GetMoves(o, Board)
#             k = random.randrange(0, len(MoveList))
#             move = MoveList[k]

#             NewBoard = SimulateMove(Board, Move=move)

#             return Rollout(Player=x, Board=NewBoard)

#         elif Player == x:
#             MoveList = GetMoves(x, Board)
#             k = random.randrange(0, len(MoveList))
#             move = MoveList[k]

#             NewBoard = SimulateMove(Board, Move=move)

#             return Rollout(Player=o, Board=NewBoard)


# # Backpropogate the value of the game up to the root.
# def BackPropogate(Node, Win):
#     # Keep going up the tree until no node exists:
#     while Node is not None:
#         # Update node visits:
#         Node.simulations += 1

#         # Update node wins:
#         Node.wins += Win

#         # Set current node to parent node:
#         Node = Node.parent_node


# # Select the most promising node.
# def Select(Node, Player):
#     while not Node.is_terminal:
#         if not Node.is_expanded:
#             Expand(
#                 Node=Node,
#                 Player=Player,
#             )
#             node = GetBestNode(Node)

#             return node


# # Expand the node if not expanded.
# def Expand(Node, Player):
#     # get all possible moves from current state (Node)
#     moves = GetMoves(Board=Node.board, Player=Player)

#     # for each move, generate new states (boards);
#     # for each state, create new child nodes;
#     # add child nodes to parent node.
#     for move in moves:
#         new_board = SimulateMove(
#             Board=Node.board,
#             Move=move,
#         )

#         child_node = TreeNode(
#             Board=new_board,
#             ParentNode=Node,
#         )

#         Node.children.append(child_node)

#     if len(moves) == len(Node.children):
#         Node.is_expanded == True

#     # return Node


# # An equation for the selection policy in the GetBestNode function.
# def UCB1(ParentNode, ChildNode) -> float:
#     if ChildNode.simulations > 0:
#         exploitation = ChildNode.wins / ChildNode.simulations

#         exploration_constant = 1.4
#         exploration = exploration_constant * math.sqrt(
#             math.log(ParentNode.simulations) / ChildNode.simulations
#         )

#         return exploitation + exploration

#     else:
#         return infinity


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

    while True:
        HvA_or_AvA = int(input("1 - Human vs AI |*| 2 - AI vs AI: "))
        if HvA_or_AvA == 1 or HvA_or_AvA == 2:
            break
        else:
            print("Enter valid option.")

    if HvA_or_AvA == 1:
        # player_move = None
        # player_chosen_symbol = None

        while True:
            player_move = int(input("1 - First Move |*| 2 - Second Move: "))
            break

        while True:
            player_chosen_symbol = int(input("1 for 'o' |*| -1 for 'x': "))
            break

        print("\nThe squares of the board are numbered by row and column, with '1 1' ")
        print("in the upper left corner, '1 2' directly to the right of '1 1', etc.")
        print("")
        print("Moves are of the form 'i j m n', where (i,j) is a square occupied")
        print("by your piece, and (m,n) is the square to which you move it.")
        print("")
        print("You move the 'X' pieces.\n")

        InitBoard(Board)
        ShowBoard(Board)

        if player_move == 1:
            for n in range(5):
                states_evaluated = 0
                MoveList = GetMoves(player_chosen_symbol, Board)
                print(MoveList)
                MoveList = GetMoves(-player_chosen_symbol, Board)
                print(MoveList)

                Move = GetHumanMove(player_chosen_symbol, Board)
                Board = ApplyMove(Board, Move)
                ShowBoard(Board)
                Move = GetComputerMove(-player_chosen_symbol, Board)

                function_time = timeit.timeit(
                    stmt="GetComputerMove(-player_chosen_symbol, Board)",
                    globals=globals(),
                    number=1,
                )

                Board = ApplyMove(Board, Move)
                ShowBoard(Board)

                print("States Evaluated: " + str(states_evaluated))
                print("time: " + str(function_time))
                print("Max Depth: " + str(max_depth))

        else:
            for n in range(5):
                states_evaluated = 0
                MoveList = GetMoves(player_chosen_symbol, Board)
                print(MoveList)
                MoveList = GetMoves(-player_chosen_symbol, Board)
                print(MoveList)

                Move = GetComputerMove(-player_chosen_symbol, Board)

                function_time = timeit.timeit(
                    stmt="GetComputerMove(-player_chosen_symbol, Board)",
                    globals=globals(),
                    number=1,
                )

                print("States Evaluated: " + str(states_evaluated))
                print("time: " + str(function_time))
                print("Max Depth: " + str(max_depth))

                Board = ApplyMove(Board, Move)
                ShowBoard(Board)

                Move = GetHumanMove(player_chosen_symbol, Board)
                Board = ApplyMove(Board, Move)
                ShowBoard(Board)

    elif HvA_or_AvA == 2:
        print("\nThe squares of the board are numbered by row and column, with '1 1' ")
        print("in the upper left corner, '1 2' directly to the right of '1 1', etc.")
        print("")
        print("Moves are of the form 'i j m n', where (i,j) is a square occupied")
        print("by your piece, and (m,n) is the square to which you move it.")
        print("")
        print("You move the 'X' pieces.\n")

        InitBoard(Board)
        ShowBoard(Board)

        for n in range(5):
            states_evaluated = 0
            MoveList = GetMoves(x, Board)
            print(MoveList)
            MoveList = GetMoves(o, Board)
            print(MoveList)

            Move = GetComputerMove(o, Board)

            function_time = timeit.timeit(
                stmt="GetComputerMove(o, Board)",
                globals=globals(),
                number=1,
            )

            Board = ApplyMove(Board, Move)
            ShowBoard(Board)

            print("States Evaluated: " + str(states_evaluated))
            print("time: " + str(function_time))
            print("Max Depth: " + str(max_depth))

            states_evaluated = 0

            Move = GetComputerMove(o, Board)
            function_time = timeit.timeit(
                stmt="GetComputerMove(o, Board)",
                globals=globals(),
                number=1,
            )

            Board = ApplyMove(Board, Move)
            ShowBoard(Board)

            print("States Evaluated: " + str(states_evaluated))
            print("time: " + str(function_time))
            print("Max Depth: " + str(max_depth))
