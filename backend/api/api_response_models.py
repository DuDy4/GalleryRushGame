from typing import List
from utils.models import Grid
from pydantic import BaseModel

class GridResponse(BaseModel):
    grid: Grid
    steps: int

    @classmethod
    def from_grid(cls, grid: Grid, steps):
        return cls(grid=grid, steps=steps)

