import hashlib

from utils.models import GridType, WinException

class GridNode:

    def __init__(self, grid: GridType, next_node: GridType | None = None):
        self.grid: GridType = grid
        self.next = next_node


class InMemoryGridChain:
    """
    I decided to implement the "time-reversal"/"step back" in a linked list, as the common methods will be
    push and pop. Each step will need one node, so a Stack structure should be useful.

    In addition, the class has a "hash set" that will save all hashings of the grids that were inserted to
    the stack/linked list. That will allow us to detect if we are in a cycle or a static grid-state.
    """
    def __init__(self):
        self.head: GridNode | None = None
        self.length = 0
        self.hash_set = set()

    def hash_grid(self, grid: GridType) -> str:
        """
        This method takes the grid (list of lists of ints), cast it to string and hashing it -
        so it could be added to the self.hash_set.

        :param grid:
        :return: str
        """
        grid_str = ''.join(''.join(map(str, row)) for row in grid)
        return hashlib.md5(grid_str.encode()).hexdigest()

    def check_win(self, grid: GridType):
        """
        This method checks if the hashing of this table is already present in the self.hash_set.
        If so, that it's a cycle or a static grid-state.

        :param grid:
        :return:
        """
        grid_hash = self.hash_grid(grid)
        if grid_hash in self.hash_set:
            return True
        self.hash_set.add(grid_hash)
        return False

    def pop_hash(self, grid: GridType) -> None:
        """
        This method pop a hash.
        That method is called when popping a grid from the stack, therefore should be removed from the
        hash_set too (to avoid win condition on the next step).

        :param grid:
        :return:
        """
        grid_hash = self.hash_grid(grid)
        self.hash_set.remove(grid_hash)

    def push(self, node: GridNode) -> bool:
        """
        This method does two main functions:
        1. Push the node to the stack.
        2. **secretly** check for win conditions, and return True upward.

        :param node:
        :return: bool:
        """
        if self.check_win(node.grid):
            return True
        if not isinstance(node,GridNode):
            return False
        if not self.head:
            self.head = node
            self.length += 1
            return False
        node.next = self.head
        self.head = node
        self.length += 1
        return False

    def pop(self) -> GridType:
        """
        This method pop a grid from the stack, and also calls to remove its hash from the self.hash_set

        :return: GridType (that was inside the node removed)
        """
        if not self.head:
            return
        if self.length <= 0:
            return
        last_grid_node = self.head
        self.head = last_grid_node.next
        self.length -= 1
        self.pop_hash(last_grid_node.grid)
        return last_grid_node.grid

    def reset(self) -> None:
        """
        Clean all 3 attributes of the class - to start a new grid (randomized or cleared)
        :return:
        """
        self.head = None
        self.length = 0
        self.hash_set.clear()