import pytest
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.grid_service import GridService

@pytest.mark.parametrize("grid_fixture_name", [
    "sample_grid",
    "diagonal_grid",
    "empty_grid",
    "full_grid"
])
def test_count_neighbors_range(grid_service, request, grid_fixture_name):
    grid = request.getfixturevalue(grid_fixture_name)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            count = grid_service.count_neighbors(grid, x, y)
            assert 0 <= count <= 8, f"Invalid neighbor count: {count} at ({x},{y})"

@pytest.mark.parametrize("grid_fixture_name", [
    "sample_grid",
    "diagonal_grid",
    "empty_grid",
    "full_grid"
])
def test_next_step_shape_preserved(grid_service, request, grid_fixture_name):
    grid = request.getfixturevalue(grid_fixture_name)
    new_grid = grid_service.next_step(grid)

    assert len(new_grid) == len(grid)
    for row in new_grid:
        assert len(row) == len(grid[0])

def test_randomize_grid_creates_valid_grid(grid_service):
    grid = grid_service.randomize_grid()
    assert len(grid) > 0
    assert all(len(row) == len(grid[0]) for row in grid)
    assert all(cell in [0, 1] for row in grid for cell in row)
