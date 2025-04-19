from utils.models import GridType
from classes.grid import Grid
from classes.in_memory_grid_chain import InMemoryGridChain, GridNode


# grid = [[0 for _ in range(CURRENT_SIZE)] for _ in range(CURRENT_SIZE)]
class GridService:

    def __init__(self):
        self.grid_instance: Grid = Grid()
        self.grid_memo: InMemoryGridChain = InMemoryGridChain()

    def get_grid_attributes(self):
        return self.grid_instance.get_grid_attributes()

    def randomize_grid(self) -> GridType:
        self.grid_memo.reset()
        return self.grid_instance.randomize_grid()


    def next_step(self) -> GridType:
        self.grid_memo.push(GridNode(self.grid_instance.grid))
        return self.grid_instance.next_step()

    def clear(self) -> GridType:
        self.grid_memo.reset()
        return self.grid_instance.clear()

    def update_cell(self, i, j):
        self.grid_instance.update_cell(i, j)

    def update_wrap(self):
        self.grid_instance.update_wrap()
