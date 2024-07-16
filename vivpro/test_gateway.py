import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from gateway import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_data():
    return {
            "id": {
                    "0": "5vYA1mW9g2Coh1HUFUSmlb",
                    "1": "2klCjJcucgGQysgH170npL",
                    "2": "093PI3mdUvOSlvMYDwnV1e",
                    "3": "64yrDBpcdwEdNY9loyEGbX",
                    "4": "2jiI8bNSDu7UxTtDCOqh3L"
                },
            "title": {
                    "0": "3AM",
                    "1": "4 Walls",
                    "2": "11:11",
                    "3": "21 Guns",
                    "4": "21"
                }
            }

@pytest.mark.asyncio
async def test_process_and_save_data(test_data):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/process_and_save_data", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data processed and saved successfully"}

@pytest.mark.asyncio
async def test_get_data_no_filter():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/get_data?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 10
    assert isinstance(data["data"], list)

@pytest.mark.asyncio
async def test_get_data_with_filter():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/get_data?title=21 Guns&page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 10
    assert len(data["data"]) == 1
    assert data["data"][0]["title"] == "21 Guns"

@pytest.mark.asyncio
async def test_get_data_pagination():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/get_data?page=1&size=1")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 1
    assert len(data["data"]) == 1

@pytest.mark.asyncio
async def test_rate_song():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/rate_song/21 Guns/5")
    assert response.status_code == 200
    assert response.json() == {"message": "Song rated successfully"}

