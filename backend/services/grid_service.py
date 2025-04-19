from utils.models import GridType
from classes.grid import Grid
from classes.in_memory_grid_chain import InMemoryGridChain, GridNode


# grid = [[0 for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
class GridService:

    def __init__(self):
        self.grid_instance: Grid = Grid()
        self.grid_memo: InMemoryGridChain = InMemoryGridChain()

    def get_grid_attributes(self) -> [GridType, int, bool]:
        return self.grid_instance.get_grid_attributes()

    def randomize_grid(self) -> [GridType, int, bool]:
        self.grid_memo.reset()
        return self.grid_instance.randomize_grid()


    def next_step(self) -> [GridType, int, bool]:
        self.grid_memo.push(GridNode(self.grid_instance.grid))
        return self.grid_instance.next_step()

    def previous_step(self) -> [GridType, int, bool]:
        if self.grid_instance.steps <= 0 or self.grid_memo.length <= 0:
            return self.grid_instance.get_grid_attributes()
        previous_grid = self.grid_memo.pop()
        return self.grid_instance.previous_step(previous_grid)

    def clear(self) -> [GridType, int, bool]:
        self.grid_memo.reset()
        return self.grid_instance.clear()

    def update_cell(self, i, j):
        self.grid_instance.update_cell(i, j)

    def update_wrap(self):
        self.grid_instance.update_wrap()
