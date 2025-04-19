from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from services.grid_service import GridService
from api.api_response_models import GridResponse
from starlette.responses import JSONResponse

router = APIRouter(prefix="/api")

grid_service = GridService()


@router.get("/", response_model=GridResponse)
async def get_current_grid() -> GridResponse:
    """
    Get the current grid in the server
    :return: GridResponse
    """
    logger.info(f"Got touch request")
    return GridResponse.from_grid(grid_service.grid, grid_service.steps)

@router.post("/randomize", response_model=GridResponse)
async def get_random_grid() -> GridResponse:
    """
    Get a new randomize grid_service.py.
    """
    logger.info(f"Got a randomize grid request")
    return GridResponse.from_grid(grid_service.randomize_grid(), 0)


@router.post("/next", response_model=GridResponse)
async def get_next_step() -> GridResponse:
    """
    Compute the next grid step and return it.
    """
    logger.info("Received next step request")
    grid_service.next_step()
    return GridResponse.from_grid(grid_service.grid, grid_service.steps)


@router.post("/clear", response_model=GridResponse)
async def clear_grid() -> GridResponse:
    """
    Clear the grid to all zeros.
    """
    logger.info("Received clearing request")
    return GridResponse.from_grid(grid_service.clear(), 0)

@router.put("/update", response_model=dict)
async def update_grid(request: Request) -> JSONResponse | HTTPException:
    """
    Update the grid manually by the user (toggling)
    :return:
    """
    try:
        payload = await request.json()
        position = payload.get("position")
        if not position or len(position) != 2:
            raise HTTPException(status_code=400, detail="Invalid or missing 'position' in payload")
        i, j = position[0], position[1]
        grid_service.update_cell(i, j)
        logger.info(f"Updated cell in position [{i}][{j}]")
        return JSONResponse(status_code=200, content="Updated grid successfully")
    except Exception as e:
        logger.error(f"Error while updating grid: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

