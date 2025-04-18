from fastapi import APIRouter
from loguru import logger
from services.grid import GridService
from api.api_response_models import GridResponse

router = APIRouter(prefix="/api")

grid_service = GridService()

@router.get("/randomize", response_model=GridResponse)
def get_random_grid() -> GridResponse:
    """
    Get a new randomize grid.py.
    """
    logger.info(f"Got a randomize grid request")
    return GridResponse.from_grid(grid_service.randomize_grid())

