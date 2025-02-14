import pygame
import random

WIDTH, HEIGHT = 700, 800
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
MINES_COUNT = 15

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MineSweeper")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Create the grid
class Cell:
    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.revealed = False
        self.flagged = False
        self.neighbor_mines = 0
    
    def draw(self, win):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(win, GRAY if self.revealed else WHITE, rect)
        pygame.draw.rect(win, BLACK, rect, 2)
        
        if self.revealed:
            if self.is_mine:
                pygame.draw.circle(win, RED, rect.center, CELL_SIZE // 3)
            elif self.neighbor_mines > 0:
                text = font.render(str(self.neighbor_mines), True, BLACK)
                win.blit(text, (self.x * CELL_SIZE + CELL_SIZE // 3, self.y * CELL_SIZE + CELL_SIZE // 4))
        elif self.flagged:
            text = font.render("F", True, BLACK)
            win.blit(text, (self.x * CELL_SIZE + CELL_SIZE // 3, self.y * CELL_SIZE + CELL_SIZE // 4))

# Initialize grid
def create_grid():
    grid = [[Cell(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
    mines = random.sample([(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)], MINES_COUNT)
    
    for x, y in mines:
        grid[x][y].is_mine = True
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if not grid[x][y].is_mine:
                grid[x][y].neighbor_mines = sum(grid[nx][ny].is_mine for nx in range(max(0, x-1), min(GRID_SIZE, x+2))
                                                for ny in range(max(0, y-1), min(GRID_SIZE, y+2)))
    
    return grid

def reveal(grid, x, y):
    if grid[x][y].revealed or grid[x][y].flagged:
        return
    
    grid[x][y].revealed = True
    
    if grid[x][y].neighbor_mines == 0 and not grid[x][y].is_mine:
        for nx in range(max(0, x-1), min(GRID_SIZE, x+2)):
            for ny in range(max(0, y-1), min(GRID_SIZE, y+2)):
                if not grid[nx][ny].revealed:
                    reveal(grid, nx, ny)

def main():
    run = True
    grid = create_grid()

    while run:
        win.fill(WHITE)
        for row in grid:
            for cell in row:
                cell.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= CELL_SIZE
                y //= CELL_SIZE
                if event.button == 1:  # Left click
                    reveal(grid, x, y)
                elif event.button == 3:  # Right click
                    grid[x][y].flagged = not grid[x][y].flagged

    pygame.quit()

if __name__ == "__main__":
    main()
