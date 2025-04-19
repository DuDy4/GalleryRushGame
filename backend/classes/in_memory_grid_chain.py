from utils.models import GridType

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

    def push(self, node: GridNode):
        if not isinstance(node,GridNode):
            return
        if not self.head:
            self.head = node
            self.length += 1
            return
        node.next = self.head
        self.head = node
        self.length += 1
        return

    def pop(self):
        if not self.head:
            return
        if self.length <= 0:
            return
        last_grid_node = self.head
        self.head = last_grid_node.next
        self.length -= 1
        return last_grid_node

    def reset(self):
        self.head = None
        self.length = 0