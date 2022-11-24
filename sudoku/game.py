import sys
import pygame
import grid as g

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

def main():
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("Sudoku")
    grid = g.Grid(720, 720, 9, 9, screen)
    pygame.display.update()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.solve()

        grid.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()

sys.exit()

