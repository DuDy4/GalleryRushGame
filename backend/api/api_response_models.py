from utils.models import GridType
from pydantic import BaseModel

class GridResponse(BaseModel):
    grid: GridType
    steps: int
    wrap: bool

    @classmethod
    def from_grid(cls, grid: GridType, steps: int, wrap: bool):
        return cls(grid=grid, steps=steps, wrap=wrap)

class WinGridResponse(BaseModel):
    grid: GridType
    steps: int
    wrap: bool
    win_reason: str

    @classmethod
    def from_grid(cls, grid: GridType, steps: int , wrap: bool, reason: str):
        return cls(grid=grid, steps=steps, wrap=wrap, win_reason=reason)