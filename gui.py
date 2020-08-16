import sys, pygame
from main import solve, print_board


test_board = [[0, 0, 2, 1, 7, 0, 0, 0, 6],
              [0, 9, 0, 0, 0, 8, 0, 5, 3],
              [0, 4, 0, 3, 0, 0, 0, 1, 8],
              [0, 0, 0, 8, 0, 0, 6, 4, 0],
              [9, 8, 0, 0, 2, 7, 0, 0, 1],
              [0, 0, 3, 0, 9, 0, 0, 2, 7],
              [5, 0, 1, 9, 0, 0, 0, 7, 0],
              [0, 7, 0, 4, 5, 1, 9, 6, 0],
              [4, 2, 9, 0, 3, 0, 0, 0, 0]]

solved_board = [[0, 0, 2, 1, 7, 0, 0, 0, 6],
              [0, 9, 0, 0, 0, 8, 0, 5, 3],
              [0, 4, 0, 3, 0, 0, 0, 1, 8],
              [0, 0, 0, 8, 0, 0, 6, 4, 0],
              [9, 8, 0, 0, 2, 7, 0, 0, 1],
              [0, 0, 3, 0, 9, 0, 0, 2, 7],
              [5, 0, 1, 9, 0, 0, 0, 7, 0],
              [0, 7, 0, 4, 5, 1, 9, 6, 0],
              [4, 2, 9, 0, 3, 0, 0, 0, 0]]

solve(solved_board)
#constats
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

class Grid:
    def __init__(self, width, height, cols, rows, screen):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.cols = cols
        self.rows = rows
        self.cubes = [[Cube(i, j, test_board[i][j], width, height, screen) for j in range(cols)] for i in range(rows)]
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

    def update(self):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[i])):
                self.cubes[i][j].value = test_board[i][j]


class Cube:
    def __init__(self, row, col, value, width, height, screen):
        self.row = row
        self.col = col
        self.value = value
        self.width = width
        self.height = height
        self.screen = screen
        self.selected = False
        self.temp_value = None

    def draw(self):
        off_set = int(self.width / 9)
        x = self.col * off_set
        y = self.row * off_set

        if self.temp_value:
            font = pygame.font.SysFont("Times New Roman", 28)
            temp_number = font.render(str(self.temp_value), 1, BLACK)
            self.screen.blit(temp_number, (x+3 , y+3))
        if self.value != 0:
            font = pygame.font.SysFont("Times New Roman", 36)
            value_number = font.render(str(self.value), 1, BLACK)
            self.screen.blit(value_number, (x + (off_set//2 - value_number.get_width()//2), y + (off_set//2 - value_number.get_height()//2)))

        if self.selected:
            red_square_thickness = 4
            pygame.draw.line(self.screen, RED, (y,x), (y, x+off_set), red_square_thickness)
            pygame.draw.line(self.screen, RED, (y,x), (y+off_set, x), red_square_thickness)
            pygame.draw.line(self.screen, RED, (y+off_set,x+off_set), (y+off_set, x), red_square_thickness)
            pygame.draw.line(self.screen, RED, (y+off_set,x+off_set), (y, x+off_set), red_square_thickness)

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
                    solve(test_board)
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
                    if solved_board[col][row] == grid.cubes[col][row].temp_value:
                        grid.cubes[col][row].value = solved_board[col][row]
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


