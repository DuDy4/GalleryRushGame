from fastapi import APIRouter
from loguru import logger
from services.grid_service import GridService
from api.api_response_models import GridResponse

router = APIRouter(prefix="/api")

grid_service = GridService()

@router.post("/randomize", response_model=GridResponse)
def get_random_grid() -> GridResponse:
    """
    Get a new randomize grid_service.py.
    """
    logger.info(f"Got a randomize grid request")
    return GridResponse.from_grid(grid_service.randomize_grid())


@router.post("/next", response_model=GridResponse)
def get_next_step() -> GridResponse:
    """
    Compute the next grid step and return it.
    """
    logger.info("Received request: /next")
    grid_service.grid = grid_service.next_step(grid_service.grid)
    return GridResponse.from_grid(grid_service.grid)


@router.post("/clear", response_model=GridResponse)
def clear_grid() -> GridResponse:
    """
    Clear the grid to all zeros.
    """
    logger.info("Received request: /clear")
    return GridResponse.from_grid(grid_service.clear())