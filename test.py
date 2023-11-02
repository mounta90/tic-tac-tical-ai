from win_functions.horizontal_win import HorizontalWin
from win_functions.vertical_win import VerticalWin
from win_functions.diagonal_win import DiagonalWin

board = [
    ["+", "+", "+", "+", "+", "+"],
    ["+", "_", "_", "_", "o", "+"],
    ["+", "_", "_", "o", "_", "+"],
    ["+", "_", "o", "_", "_", "+"],
    ["+", "_", "_", "_", "_", "+"],
    ["+", "_", "_", "_", "o", "+"],
    ["+", "+", "+", "+", "+", "+"],
]

value = DiagonalWin("o", board)

print(value)
