from utils.models import GridType
from pydantic import BaseModel

class GridResponse(BaseModel):
    grid: GridType
    steps: int
    wrap: bool

    @classmethod
    def from_grid(cls, grid: GridType, steps, wrap):
        return cls(grid=grid, steps=steps, wrap=wrap)

