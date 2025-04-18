import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from start_api import app

client = TestClient(app)

# Helper to send custom grid to /api/next
def send_next_step_with_grid(grid):
    return client.post("/api/next", json={"grid": grid})

def test_root_returns_ok():
    res = client.get("/")
    assert res.status_code == 200
    assert "Gallery Rush Game" in res.text

def test_randomize_endpoint_works():
    res = client.post("/api/randomize")
    assert res.status_code == 200
    data = res.json()
    assert "grid" in data
    assert len(data["grid"]) > 0

def test_clear_endpoint_returns_empty_grid():
    res = client.post("/api/clear")
    assert res.status_code == 200
    data = res.json()
    assert "grid" in data
    assert all(cell == 0 for row in data["grid"] for cell in row)

def test_next_step_after_randomize():
    client.post("/api/randomize")
    res = client.post("/api/next")
    assert res.status_code == 200
    data = res.json()
    assert "grid" in data
    assert len(data["grid"]) > 0

@pytest.mark.parametrize("grid_fixture_name", [
    "sample_grid",
    "diagonal_grid",
    "empty_grid",
    "full_grid"
])
def test_api_next_accepts_custom_grid(request, grid_fixture_name):
    grid = request.getfixturevalue(grid_fixture_name)
    res = send_next_step_with_grid(grid)
    assert res.status_code == 200
    data = res.json()
    assert "grid" in data
    assert len(data["grid"]) == len(grid)

