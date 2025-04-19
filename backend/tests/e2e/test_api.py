from fastapi.testclient import TestClient
from start_api import app

from backend.utils.models import WinReason

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

def test_wrap_endpoint_toggles_wrap_state():
    """
    Test that the wrap endpoint toggles the wrap state and returns the correct grid response.
    """
    # Get initial state
    initial_state = client.get("/api/").json()
    initial_wrap = initial_state["wrap"]
    
    # Toggle wrap state
    res = client.post("/api/wrap")
    assert res.status_code == 200
    data = res.json()
    assert "wrap" in data
    assert data["wrap"] == (not initial_wrap)
    
    # Toggle back
    res = client.post("/api/wrap")
    assert res.status_code == 200
    data = res.json()
    assert data["wrap"] == initial_wrap


def test_win_state_extinction():
    """
    This should return the WinReason.EXTINCTION value
    """
    res = client.post("/api/clear")
    assert res.status_code == 200
    res = client.post("/api/next")
    assert res.status_code == 200
    data = res.json()
    assert "win_reason" not in data.keys()

    # Now we should get the winReason
    res = client.post("/api/next")
    data = res.json()
    assert "win_reason" in data.keys()
    assert data["win_reason"] == WinReason.EXTINCTION.value

def test_win_state_static():
    """
    This should return the WinReason.STATIC value
    """
    res = client.post("/api/clear")
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [0,0]})
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [1,0]})
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [0,1]})
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [1,1]})
    assert res.status_code == 200

    res = client.post("/api/next")
    assert res.status_code == 200
    data = res.json()
    assert "win_reason" not in data.keys()

    # Now we should get the winReason
    res = client.post("/api/next")
    data = res.json()
    assert "win_reason" in data.keys()
    assert data["win_reason"] == WinReason.STATIC.value


def test_win_state_cycle():
    """
    This should return the WinReason.STATIC value
    """
    res = client.post("/api/clear")
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [0,1]})
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [1,1]})
    assert res.status_code == 200
    res = client.put("/api/update", json={"position": [2,1]})
    assert res.status_code == 200


    res = client.post("/api/next")
    assert res.status_code == 200
    data = res.json()
    assert "win_reason" not in data.keys()

    res = client.post("/api/next")
    assert res.status_code == 200
    data = res.json()
    assert "win_reason" not in data.keys()

    # Now we should get the winReason
    res = client.post("/api/next")
    data = res.json()
    assert "win_reason" in data.keys()
    assert data["win_reason"] == WinReason.CYCLE.value
