from utils.models import GridType
from random import randint

CURRENT_SIZE = 4

class Grid:

    def __init__(self):
        self.grid: GridType = None
        self.steps: int = 0
        self.wrap: bool = False
        self.randomize_grid()  # This will assign new grid to self.grid

    def get_grid_attributes(self) -> [GridType, int, bool]:
        return [self.grid, self.steps, self.wrap]

    def randomize_grid(self) -> [GridType, int, bool]:
        self.grid = [[randint(0,1) for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
        self.steps = 0
        return self.get_grid_attributes()

    def next_step(self) -> [GridType, int, bool]:
        """
        The way this method works is:
        1. Using count_neighbours (helper) function to calculate the business of the area.
        2. Apply the given logic to deduct if should close/start a gallery on this spot

        Now, take this logic and run it for every spot.

        :param:
        :return: grid:
        """

        def count_neighbors(grid: GridType, x: int, y: int) -> int:
            """
            For every cell, check all adjust cells in a 9X9 (skip itself - i=0, j=0).
            Count the sum of all of them, and if it is 4 or more - we can break the check ->
            the gallery should be closed...

            Conditional check: If `self.wrap` is enabled, it wraps around the grid edges (toroidal logic).
            If wrapping is off, it doesn't count out-of-bounds neighbors.

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
                    if self.wrap:
                        # Add i and j to indexes, and modulo by the number of cells to get to "the other side"
                        nx %= len(self.grid)
                        ny %= len(self.grid[0])
                        count += grid[nx][ny]
                    else:
                        # If not wrapping the edges
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
        return self.get_grid_attributes()

    def previous_step(self, grid: GridType):
        if self.steps <= 0:
            raise Exception("Should not have got here: Returning steps in Grid Class when there is no steps left")
        self.grid = grid
        self.steps -= 1
        return self.get_grid_attributes()

    def clear(self) -> [GridType, int, bool]:
        self.grid = [[0 for _ in range(len(self.grid))] for _ in range(len(self.grid))]
        self.steps = 0
        return self.get_grid_attributes()

    def update_cell(self, i, j):
        self.grid[i][j] = abs(self.grid[i][j] - 1)

    def update_wrap(self):
        self.wrap = not self.wrap
