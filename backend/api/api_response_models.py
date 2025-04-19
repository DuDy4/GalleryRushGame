from typing import List
from utils.models import Grid
from pydantic import BaseModel

class GridResponse(BaseModel):
    grid: Grid
    steps: int
    wrap: bool

    @classmethod
    def from_grid(cls, grid: Grid, steps, wrap):
        return cls(grid=grid, steps=steps, wrap=wrap)

