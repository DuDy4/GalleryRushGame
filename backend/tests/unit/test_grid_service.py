import pytest

@pytest.mark.parametrize("grid_fixture_name", [
    "sample_grid",
    "diagonal_grid",
    "empty_grid",
    "full_grid"
])
def test_next_step_shape_preserved(grid_service, request, grid_fixture_name):
    start_grid = grid_service.grid_instance.grid
    start_steps = grid_service.grid_instance.steps
    new_grid = grid_service.next_step()[0]

    assert len(new_grid) == len(start_grid)
    for row in new_grid:
        assert len(row) == len(start_grid[0])
    assert grid_service.grid_instance.steps == start_steps + 1

def test_randomize_grid_creates_valid_grid(grid_service):
    grid = grid_service.randomize_grid()[0]
    assert len(grid) > 0
    assert all(len(row) == len(grid[0]) for row in grid)
    assert all(cell in [0, 1] for row in grid for cell in row)

def test_update_cell_toggles_value_correctly(grid_service):
    """
    Test that update_cell toggles 0 to 1 and 1 to 0 as expected.
    """
    # Start with a clean grid
    grid_service.grid_instance.grid = [
        [0, 0],
        [0, 0]
    ]

    # Toggle (0 → 1)
    grid_service.update_cell(0, 0)
    assert grid_service.grid_instance.grid[0][0] == 1

    # Toggle again (1 → 0)
    grid_service.update_cell(0, 0)
    grid = grid_service.get_grid_attributes()[0]
    assert grid[0][0] == 0

    # Ensure no other cells were modified
    assert grid[0][1] == 0
    assert grid[1][0] == 0
    assert grid[1][1] == 0

def test_update_wrap_toggles_wrap_state(grid_service):
    """
    Test that update_wrap toggles the wrap state correctly.
    """
    initial_wrap = grid_service.grid_instance.wrap
    
    # Toggle wrap state
    grid_service.update_wrap()
    assert grid_service.grid_instance.wrap == (not initial_wrap)
    
    # Toggle back
    grid_service.update_wrap()
    assert grid_service.grid_instance.wrap == initial_wrap

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
    grid_service.grid_instance.grid = edge_pattern_grid
    assert grid_service.grid_instance.wrap == False
    grid_service.next_step()

    grid = grid_service.get_grid_attributes()[0]
    # The edge cells should die without wrapping
    assert grid[1][0] == 0
    assert grid[2][0] == 0
    assert grid[3][0] == 0
    
    # Test with wrapping
    grid_service.grid_instance.grid = edge_pattern_grid
    grid_service.update_wrap()
    assert grid_service.grid_instance.wrap == True
    grid_service.next_step()

    grid = grid_service.get_grid_attributes()[0]

    # With wrapping, the pattern should survive
    assert grid[1][0] == 1
    assert grid[2][0] == 1
    assert grid[3][0] == 1