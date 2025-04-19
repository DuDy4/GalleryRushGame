import pytest
import sys
import os

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

def test_update_cell_toggles_value_correctly():
    """
    Test that update_cell toggles 0 to 1 and 1 to 0 as expected.
    """
    # Start with a clean grid
    grid_service = GridService()
    grid_service.grid = [
        [0, 0],
        [0, 0]
    ]

    # Toggle (0 → 1)
    grid_service.update_cell(0, 0)
    assert grid_service.grid[0][0] == 1

    # Toggle again (1 → 0)
    grid_service.update_cell(0, 0)
    assert grid_service.grid[0][0] == 0

    # Ensure no other cells were modified
    assert grid_service.grid[0][1] == 0
    assert grid_service.grid[1][0] == 0
    assert grid_service.grid[1][1] == 0