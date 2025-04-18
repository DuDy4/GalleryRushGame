from typing import List

from pydantic import BaseModel

class GridResponse(BaseModel):
    grid: List[List[int]]
    steps: int

    @classmethod
    def from_grid(cls, grid: List[List[int]], steps):
        return cls(grid=grid, steps=steps)

