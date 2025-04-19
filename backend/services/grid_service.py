from typing import List
from random import randint
from utils.models import Grid

CURRENT_SIZE = 20

# grid = [[0 for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
class GridService:

    def __init__(self):
        self.grid: Grid = self.randomize_grid()
        self.steps = 0

    def randomize_grid(self) -> Grid:
        self.grid = [[randint(0,1) for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
        self.steps = 0
        return self.grid

    def count_neighbors(self, grid: Grid, x: int, y: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + i, y + j
                if 0 <= nx < len(grid) and 0 <= ny < len(grid):
                    count += grid[nx][ny]
        return count

    def next_step(self) -> Grid:
        """
        The way this method works is:
        1. Using count_neighbours (helper) function to calculate the business of the area.
        2. Apply the given logic to deduct if should close/start a gallery on this spot

        Now, take this logic and run it for every spot.

        :param:
        :return: grid:
        """

        def count_neighbors(grid: Grid, x: int, y: int) -> int:
            """
            For every cell, check all adjust cells in a 9X9 (skip itself - i=0, j=0).
            Count the sum of all, and if it is 4 or more - we can    break the check ->
            the gallery should be closed...

            :param grid:
            :param x:
            :param y:
            :return:
            """
            count = 0
            for i in range(-1, 2):
                if count > 3:
                    break
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    # nx, ny present the current neighbour position (original cell + i/j)
                    nx, ny = x + i, y + j
                    if 0 <= nx < len(grid) and 0 <= ny < len(grid):
                        count += grid[nx][ny]
            return count


        new_grid = [[0 for _ in range(len(self.grid))] for _ in range(len(self.grid))]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                neighbors = count_neighbors(self.grid, i, j)
                if self.grid[i][j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        # Should close the gallery
                        new_grid[i][j] = 0
                    else:
                        # Gallery remains active :)
                        new_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        # A great opportunity to start a gallery
                        new_grid[i][j] = 1
        self.grid = new_grid
        self.steps += 1
        return self.grid

    def clear(self) -> Grid:
        self.grid = [[0 for _ in range(len(self.grid))] for _ in range(len(self.grid))]
        self.steps = 0
        return self.grid

    def update_cell(self, i, j):
        self.grid[i][j] = abs(self.grid[i][j] - 1)


