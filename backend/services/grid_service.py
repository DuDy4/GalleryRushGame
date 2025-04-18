from typing import List
from random import randint

CURRENT_SIZE = 20

# grid = [[0 for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
class GridService:

    def __init__(self):
        self.grid = self.randomize_grid()

    def randomize_grid(self) -> List[List[int]]:
        self.grid = [[randint(0,1) for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
        return self.grid

    def count_neighbors(self, grid: List[List[int]], x: int, y: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + i, y + j
                if 0 <= nx < len(grid) and 0 <= ny < len(grid):
                    count += grid[nx][ny]
        return count

    def next_step(self, grid: List[List[int]]) -> List[List[int]]:
        new_grid = [[0 for _ in range(len(grid))] for _ in range(len(grid))]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                neighbors = self.count_neighbors(grid, i, j)
                if grid[i][j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        return self.grid

    def print_grid(self, grid: List[List[int]]) -> None:
        print(' ')
        for i in range(len(grid)):
            print(grid[i])

    def clear(self):
        self.grid = [[0 for _ in range(len(self.grid))] for _ in range(len(self.grid))]
        return self.grid

