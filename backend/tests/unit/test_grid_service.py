import pytest


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
    start_grid = grid_service.grid
    start_steps = grid_service.steps
    new_grid = grid_service.next_step()

    assert len(new_grid) == len(start_grid)
    for row in new_grid:
        assert len(row) == len(start_grid[0])
    assert grid_service.steps == start_steps + 1

def test_randomize_grid_creates_valid_grid(grid_service):
    grid = grid_service.randomize_grid()
    assert len(grid) > 0
    assert all(len(row) == len(grid[0]) for row in grid)
    assert all(cell in [0, 1] for row in grid for cell in row)

def test_update_cell_toggles_value_correctly(grid_service):
    """
    Test that update_cell toggles 0 to 1 and 1 to 0 as expected.
    """
    # Start with a clean grid
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

def test_update_wrap_toggles_wrap_state(grid_service):
    """
    Test that update_wrap toggles the wrap state correctly.
    """
    initial_wrap = grid_service.wrap
    
    # Toggle wrap state
    grid_service.update_wrap()
    assert grid_service.wrap == (not initial_wrap)
    
    # Toggle back
    grid_service.update_wrap()
    assert grid_service.wrap == initial_wrap

def test_wrap_affects_grid_evolution(grid_service, edge_pattern_grid):
    """
    Test that wrapping affects the grid evolution by using a pattern that would die without wrapping
    but survive with wrapping.

    Edge pattern grid:
        [0, 0, 0, 0]
        [0, 0, 0, 0]
        [1, 1, 0, 1]
        [0, 0, 0, 0]

    Edge pattern grid with wrapping:
        [0, 0, 0, 0]
        [1, 0, 0, 0]
        [1, 0, 0, 0]
        [1, 0, 0, 0]
    """
    # Test without wrapping
    grid_service.grid = edge_pattern_grid
    grid_service.wrap = False
    grid_service.next_step()
    
    # The edge cells should die without wrapping
    assert grid_service.grid[1][0] == 0
    assert grid_service.grid[2][0] == 0
    assert grid_service.grid[3][0] == 0
    
    # Test with wrapping
    grid_service.grid = edge_pattern_grid
    grid_service.wrap = True
    grid_service.next_step()
    
    # With wrapping, the pattern should survive
    assert grid_service.grid[1][0] == 1
    assert grid_service.grid[2][0] == 1
    assert grid_service.grid[3][0] == 1