from fastapi.testclient import TestClient
from start_api import app

client = TestClient(app)

def test_get_current_grid():
    # Ensure the server returns the current grid and step count
    res = client.get("/api/")
    assert res.status_code == 200

    data = res.json()
    assert "grid" in data
    assert isinstance(data["grid"], list)
    assert all(isinstance(row, list) for row in data["grid"])
    assert "steps" in data
    assert isinstance(data["steps"], int)

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

def test_updating_grid():
    """
    Cleaning the grid for a predictable outcome, and then testing 0 to 1 and 1 to 0
    :return:
    """

    # Clean the grid for a known state (all zeros)
    res = client.post("/api/clear")

    assert res.status_code == 200
    data = res.json()
    i, j = 1, 1
    assert data["grid"][i][j] == 0  # sanity check

    # Toggle (0 → 1)
    toggle_res1 = client.put("/api/update", json={"position": [i, j]})
    assert toggle_res1.status_code == 200
    assert toggle_res1.json() == "Updated grid successfully"

    # Verify toggle succeeded
    after_toggle1 = client.get("/api/").json()["grid"]
    assert after_toggle1[i][j] == 1

    # Toggle back (1 → 0)
    toggle_res2 = client.put("/api/update", json={"position": [i, j]})
    assert toggle_res2.status_code == 200
    assert toggle_res2.json() == "Updated grid successfully"

    after_toggle2 = client.get("/api/").json()["grid"]
    assert after_toggle2[i][j] == 0
