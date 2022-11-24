import sys
import pygame
import helpers
from copy import deepcopy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Grid:
    board = helpers.generate_puzzle()
    solved_board = deepcopy(board)
    helpers.solve(solved_board)

    def __init__(self, width, height, cols, rows, screen):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.cols = cols
        self.rows = rows
        self.cubes = [[Cube(i, j, self.board[i][j], width, height, screen) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.screen = screen
        self.draw()

    def draw(self):
        self.screen.fill(WHITE)

        for i in range(1,10):
            off_set = int(self.width / 9)

            if (i % 3 == 0):
                thickness = 4
            else:
                thickness = 2
            pygame.draw.line(self.screen, BLACK, (0, off_set * i), (720, off_set * i), width=thickness)
            pygame.draw.line(self.screen, BLACK, (off_set * i, 0), (off_set * i, 720), width=thickness)

        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[i])):
                self.cubes[i][j].draw()

    def restart_board(self):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[i])):
                self.cubes[i][j].value = self.board[i][j]

    def solve(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            self.board[i][j] = self.solved_board[i][j]
                            self.cubes[i][j].value = self.solved_board[i][j]
                    pygame.display.update()
                    return False

        if not helpers.find_first_empty_field(self.board):
            return True
        i, j = helpers.find_first_empty_field(self.board)
        cube = self.cubes[i][j]

        for num in range(1, 10):

            cube.value = num
            self.board[i][j] = num
            self.draw()
            pygame.display.update()
            if helpers.valid(self.board, j, i):

                if self.solve():
                    return True

            cube.value = 0
            self.board[i][j] = 0
            self.draw()
            pygame.display.update()

        return False

class Cube:
    def __init__(self, row, col, value, width, height, screen):
        self.row = row
        self.col = col
        self.value = value
        self.width = width
        self.height = height
        self.screen = screen
        self.off_set = int(self.width / 9)

    def draw(self):
        x = self.col * self.off_set
        y = self.row * self.off_set

        if self.value != 0:
            font = pygame.font.SysFont("Times New Roman", 36)
            value_number = font.render(str(self.value), True, BLACK)
            self.screen.blit(value_number, (x + (self.off_set//2 - value_number.get_width()//2), y + (self.off_set//2 - value_number.get_height()//2)))

