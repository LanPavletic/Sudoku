import sys
import pygame
import solving_functions
from copy import deepcopy


#constats
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

class Grid:
    board = solving_functions.generate_puzzle()
    solved_board = deepcopy(board)
    solving_functions.solve(solved_board)

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

    def select(self, x, y):
        for i in range(len(self.cubes)):
            for cube in self.cubes[i]:
                cube.selected = False

        off_set = int(self.width / 9)
        col = x // off_set
        row = y // off_set
        self.selected = (col, row)
        self.cubes[col][row].selected = True
        return (col, row)

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

        if not solving_functions.find_first_empty_field(self.board):
            return True
        i, j = solving_functions.find_first_empty_field(self.board)
        cube = self.cubes[i][j]

        for num in range(1, 10):

            cube.value = num
            self.board[i][j] = num
            self.draw()
            pygame.display.update()
            if solving_functions.valid(self.board, j, i):

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
        self.selected = False
        self.temp_value = None

    def draw(self):
        x = self.col * self.off_set
        y = self.row * self.off_set

        if self.temp_value:
            font = pygame.font.SysFont("Times New Roman", 28)
            temp_number = font.render(str(self.temp_value), 1, BLACK)
            self.screen.blit(temp_number, (x+3 , y+3))
        if self.value != 0:
            font = pygame.font.SysFont("Times New Roman", 36)
            value_number = font.render(str(self.value), 1, BLACK)
            self.screen.blit(value_number, (x + (self.off_set//2 - value_number.get_width()//2), y + (self.off_set//2 - value_number.get_height()//2)))

        if self.selected:
            self.draw_red_square()

    def draw_red_square(self):
        x = self.col * self.off_set
        y = self.row * self.off_set
        red_square_thickness = 4
        pygame.draw.line(self.screen, RED, (y,x), (y, x+self.off_set), red_square_thickness)
        pygame.draw.line(self.screen, RED, (y,x), (y+self.off_set, x), red_square_thickness)
        pygame.draw.line(self.screen, RED, (y+self.off_set,x+self.off_set), (y+self.off_set, x), red_square_thickness)
        pygame.draw.line(self.screen, RED, (y+self.off_set,x+self.off_set), (y, x+self.off_set), red_square_thickness)

def redraw(grid):
    grid.draw()


def main():
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("Sudoku")
    grid = Grid(720, 720, 9, 9, screen)
    pygame.display.update()
    run = True
    key = None


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.solve()
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE and grid.selected:
                    row, col = grid.selected
                    grid.cubes[col][row].temp_value = None
                if event.key == pygame.K_RETURN and grid.selected:
                    row, col = grid.selected
                    if grid.solved_board[col][row] == grid.cubes[col][row].temp_value:
                        grid.cubes[col][row].value = grid.solved_board[col][row]
                        grid.cubes[col][row].temp_value = None


            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid.select(x, y)

            if grid.selected and key:
                row, col = grid.selected
                if grid.cubes[col][row].value == 0:
                    grid.cubes[col][row].temp_value = key
                key = None

        redraw(grid)
        pygame.display.update()

if __name__ == "__main__":
    main()


sys.exit()
