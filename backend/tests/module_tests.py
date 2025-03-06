from fastapi import responses
import pytest
from fastapi.testclient import TestClient
from ..main_router import app


client = TestClient(app=app)

@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "sjdhsad"
    ]
)
def test_min_steambuy(name):
    response = client.get(f"/get_min_steambuy/{name}")
    assert response.status_code == 200
    assert response.json() != None


@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "adsalkdkasd"
    ]
)
def test_max_steambuy(name):
    response = client.get(f"/get_max_steambuy/{name}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "aksdjsakjdsad"
    ]
)
def test_min_steam_account(name):
    response = client.get(f"/get_min_steam_account/{name}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "kbdjfbdfk"
    ]
)
def test_max_steam_account(name):
    response = client.get(f"/get_max_steam_account/{name}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "asdlsadsald"
    ]
)
def test_min_plati(name):
    response = client.get(f"/min_plati/{name}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "asjdsajdsalkdsa"
    ]
)
def test_max_plati(name):
    response = client.get(f"/max_plati/{name}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name",
    [
        "grand theft auto",
        "counter strike",
        "miside",
        "elden ring",
        "roblox",
        "dark souls 3",
        "death stranding",
        "ospdsofspodfpoidsf"
    ]
)
def test_popular_plati(name):
    response = client.get(f"/most_popular_plati/{name}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name, min, max",
    [
        ("grand theft auto", "1000", "5000"),
        ("counter strike", "1000", "5000"),
        ("miside", "1000", "5000"),
        ("elden ring", "1000", "5000"),
        ("roblox", "1000", "5000"),
        ("dark souls 3", "1000", "5000"),
        ("death stranding", "1000", "5000"),
        ("ooosisisjsjsj", "1000", "5000")
    ]
)
def test_range_plati(name, min, max):
    response = client.get(f"/get_range_plati/{name}&min={min}&max={max}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name, min, max",
    [
        ("grand theft auto", "1000", "5000"),
        ("counter strike", "1000", "5000"),
        ("miside", "1000", "5000"),
        ("elden ring", "1000", "5000"),
        ("roblox", "1000", "5000"),
        ("dark souls 3", "1000", "5000"),
        ("death stranding", "1000", "5000"),
        ("ooosisisjsjsj", "1000", "5000")
    ]
)
def test_range_steambuy(name, min, max):
    response = client.get(f"/get_range_steambuy/{name}&min={min}&max={max}")
    assert response.status_code == 200
    assert response.json() != None

@pytest.mark.parametrize(
    "name, min, max",
    [
        ("grand theft auto", "1000", "5000"),
        ("counter strike", "1000", "5000"),
        ("miside", "1000", "5000"),
        ("elden ring", "1000", "5000"),
        ("roblox", "1000", "5000"),
        ("dark souls 3", "1000", "5000"),
        ("death stranding", "1000", "5000"),
        ("ooosisisjsjsj", "1000", "5000")
    ]
)
def test_range_steam_accounts(name, min, max):
    response = client.get(f"/get_range_steam_accounts/{name}&min={min}&max={max}")
    assert response.status_code == 200
    assert response.json() != None
