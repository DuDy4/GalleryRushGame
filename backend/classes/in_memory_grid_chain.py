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
    """
    def __init__(self):
        self.head: GridNode | None = None
        self.length = 0
        self.hash_set = set()

    def hash_grid(self, grid: GridType) -> str:
        grid_str = ''.join(''.join(map(str, row)) for row in grid)
        return hashlib.md5(grid_str.encode()).hexdigest()

    def check_win(self, grid: GridType):
        grid_hash = self.hash_grid(grid)
        if grid_hash in self.hash_set:
            return True
        self.hash_set.add(grid_hash)
        return False

    def pop_hash(self, grid: GridType):
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
        self.head = None
        self.length = 0
        self.hash_set.clear()