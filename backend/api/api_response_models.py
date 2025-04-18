from typing import List

from pydantic import BaseModel

class GridResponse(BaseModel):
    grid: List[List[int]]

    @classmethod
    def from_grid(cls, grid: List[List[int]]):
        return cls(grid=grid)

