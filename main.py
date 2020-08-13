import random

board2 = [[0, 0, 2, 1, 7, 0, 0, 0, 6],
          [0, 9, 0, 0, 0, 8, 0, 5, 3],
          [0, 4, 0, 3, 0, 0, 0, 1, 8],
          [0, 0, 0, 8, 0, 0, 6, 4, 0],
          [9, 8, 0, 0, 2, 7, 0, 0, 1],
          [0, 0, 3, 0, 9, 0, 0, 2, 7],
          [5, 0, 1, 9, 0, 0, 0, 7, 0],
          [0, 7, 0, 4, 5, 1, 9, 6, 0],
          [4, 2, 9, 0, 3, 0, 0, 0, 0]]

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

def rotate_board_180(board):
    new_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(9):
        for j in range(9):
            new_board[i][j] = board[9-j-1][9-i-1]
    return new_board


def filled(board):
    count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                count += 1
    if count > 0:
        return False
    else:
        return True

def candidates(board, x, y):
    candidates = []
    for i in range(1, 10):
        board[y][x] = i
        if valid(board, x ,y):
            candidates.append(i)
    board[y][x] = 0
    return candidates

def field_with_fewest_possible_candidates(board):
    count = 10
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                num_of_canidates = len(candidates(board, j, i))
                if num_of_canidates < count:
                    count = num_of_canidates
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
    #if no empty fields were found aka the board is solved
    return False

def valid(board, x, y):
    #checks row for the same number
    if board[y].count(board[y][x]) > 1:
        return False
    #checks column for the same number
    for i, row in enumerate(board):
        if row[x] == board[y][x] and i != y:
            return False

    x_start = x - x % 3
    x_end = x_start + 2
    y_start= y - y % 3
    y_end = y_start + 2


    #checks the 3x3 box for the same number
    for i in range(len(board[y_start : y_end+1])):
        for j in range(len(board[i][x_start : x_end+1])):
            if board[y][x] == board[i+y_start][j+x_start] and j+x_start != x and i+x_start != y:
                return False
    return True

def solve(board):
    if not find_first_empty_field(board):
        return True

    y, x = find_first_empty_field(board)

    for num in range(1,10):
        board[y][x] = num
        if valid(board, x, y):
            if solve(board):
                return True
        board[y][x] = 0
    return False

def solveable(board):

    board_cpy = board[:]

    if solve(board_cpy):
        return True
    else:
        return False

def generate_board(board):

    if filled(board):
        return True
    x, y = field_with_fewest_possible_candidates(board)
    list_of_candidates = candidates(board, x, y)

    while list_of_candidates != []:
        board[y][x] = list_of_candidates[random.randint(0, len(list_of_candidates) - 1)]
        list_of_candidates.remove(board[y][x])

        if valid(board, x, y):
            if generate_board(board):
                return True
    board[y][x] = 0
    return False


def generate_puzzle(board):
    generate_board(board)

    start_x, start_y = random.randint(0, 8), random.randint(0, 8)
    board[start_y][start_x] = 0
    print_board(board)
    print(" ")

    i = 0
    while i < 50:
        while True:
            start_x_cpy = start_x
            start_y_cpy = start_y

            start_x += random.randrange(-1, 2)
            start_y += random.randrange(-1, 2)

            if not (0 <= start_x <= 8 and 0 <= start_y <= 8):
                start_x = start_x_cpy
                start_y = start_y_cpy
            else:
                break

        cpy = board[start_y][start_x]
        board[start_y][start_x] = 0
        board_cpy = board
        if solve(board) and solve(rotate_board_180(board)):
            board = board_cpy
            i += 1
        else:
            board[start_y][start_x] = cpy

print(solveable(board2))
print_board(board2)
