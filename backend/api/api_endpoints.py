from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from services.grid_service import GridService
from api.api_response_models import GridResponse, WinGridResponse
from starlette.responses import JSONResponse
from utils.models import WinException

router = APIRouter(prefix="/api")

grid_service = GridService()


@router.get("/", response_model=GridResponse)
async def get_current_grid() -> GridResponse:
    """
    Get the current state of the grid.
    
    Returns:
        GridResponse: The current grid state including the grid data and number of steps taken
    """
    logger.info(f"Got touch request")
    return GridResponse.from_grid(*grid_service.get_grid_attributes())

@router.post("/randomize", response_model=GridResponse)
async def get_random_grid() -> GridResponse:
    """
    Generate a new randomized grid.

    Returns:
        GridResponse: A new randomly generated grid (with step count of 0)
    """
    logger.info(f"Got a randomize grid request")
    return GridResponse.from_grid(*grid_service.randomize_grid())


@router.post("/next", response_model=GridResponse | WinGridResponse)
async def get_next_step() -> GridResponse | WinGridResponse:
    """
    Compute and return the next step in the grid's evolution.
    
    Returns:
        GridResponse: The grid state after computing the next step
    """
    try:
        logger.info("Received next step request")
        return GridResponse.from_grid(*grid_service.next_step())
    except WinException as e:
        logger.info(f"Player won! {e.reason.value}")
        return WinGridResponse.from_grid(*grid_service.get_grid_attributes(), e.reason.value)


@router.post("/previous", response_model=GridResponse)
async def get_previous_step() -> GridResponse:
    """
    Popping the previous step from memory.

    Returns:
        GridResponse: The grid state of the previous step
    """
    logger.info("Received previous step request")
    return GridResponse.from_grid(*grid_service.previous_step())


@router.post("/clear", response_model=GridResponse)
async def clear_grid() -> GridResponse:
    """
    Reset the grid to *all zeros* state.
    
    Returns:
        GridResponse: The cleared grid (with step count of 0)
    """
    logger.info("Received clearing request")
    return GridResponse.from_grid(*grid_service.clear())

@router.put("/update", response_model=dict)
async def update_grid(request: Request) -> JSONResponse | HTTPException:
    """
    Update a specific cell in the grid to the opposite value.
    
    Args:
        request (Request): The request containing the position to update
        
    Request Body:
        {
            "position": [int, int]  # The [i, j] coordinates of the cell to update
        }
        
    Returns:
        JSONResponse: Success message if update was successful
        
    Raises:
        HTTPException: 400 if position is invalid or missing
        HTTPException: 500 if an internal error occurs
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


@router.post("/wrap", response_model=GridResponse)
async def update_wrap() -> GridResponse:
    """
    This should toggle the wrap attribute, affecting the computing of next steps.
    :return:
    """
    grid_service.update_wrap()
    return GridResponse.from_grid(*grid_service.get_grid_attributes())


