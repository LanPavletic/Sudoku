import random
from copy import deepcopy

def rotate_board_180(board):
    board_cpy = deepcopy(board)
    for i in range(9):
        for j in range(9):
            board[i][j] = board_cpy[8 - i][8 - j]


def filled(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True


def candidates(board, x, y):
    _candidates = []
    for i in range(1, 10):
        board[y][x] = i
        if valid(board, x, y):
            _candidates.append(i)
    board[y][x] = 0
    return _candidates


def field_with_fewest_possible_candidates(board):
    count = 10
    x = 0
    y = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                num_of_candidates = len(candidates(board, j, i))
                if num_of_candidates < count:
                    count = num_of_candidates
                    x, y = j, i
    return x, y


def valid_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0 and not valid(board, j, i):
                return False
    return True


def print_board(board):
    for row in board:
        print(row)


def find_first_empty_field(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    # if no empty fields were found aka the board is solved
    return -1, -1 


def valid(board, x, y):
    # checks row for the same number
    if board[y].count(board[y][x]) > 1:
        return False
    # checks column for the same number
    for i, row in enumerate(board):
        if row[x] == board[y][x] and i != y:
            return False

    x_start = x - x % 3
    x_end = x_start + 2
    y_start = y - y % 3
    y_end = y_start + 2

    # checks the 3x3 box for the same number
    for i in range(len(board[y_start: y_end + 1])):
        for j in range(len(board[i][x_start: x_end + 1])):
            if board[y][x] == board[i + y_start][j + x_start] and j + x_start != x and i + x_start != y:
                return False
    return True


def solve(board):
    if not valid_board(board):
        return False
    if not find_first_empty_field(board):
        return True

    y, x = find_first_empty_field(board)
    
    if y == -1 or x == -1:
       return True; 

    for num in range(1, 10):
        board[y][x] = num
        if valid(board, x, y):
            if solve(board):
                return True
        board[y][x] = 0
    return False


def generate_board(board):
    if filled(board):
        return True
    x, y = field_with_fewest_possible_candidates(board)
    list_of_candidates = candidates(board, x, y)

    while list_of_candidates:
        board[y][x] = list_of_candidates[random.randint(0, len(list_of_candidates) - 1)]
        list_of_candidates.remove(board[y][x])

        if valid(board, x, y):
            if generate_board(board):
                return True
    board[y][x] = 0
    return False

def solvable(board):

    board_cpy1 = deepcopy(board)
    board_cpy2 = deepcopy(board)

    solve(board_cpy1)
    rotate_board_180(board_cpy2)
    solve(board_cpy2)
    rotate_board_180(board_cpy2)
    return board_cpy2 == board_cpy1

def generate_puzzle():
    board = [[0 for _ in range(9)] for _ in range(9)]
    generate_board(board)

    i = 0
    while i < 50:
        start_x, start_y = random.randint(0, 8), random.randint(0, 8)
        if not (board[start_y][start_x] == 0):
            value = board[start_y][start_x]
            board[start_y][start_x] = 0

            if solvable(board):
                i += 1
            else:
                board[start_y][start_x] = value
    return board
