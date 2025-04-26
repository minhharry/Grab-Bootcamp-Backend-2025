from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_create_dummy():
    payload = {
        "name": "Test Dummy",
        "value": 123
    }
    response = client.post("/dummy/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "item" in data
    assert data["item"]["name"] == "Test Dummy"
    assert data["item"]["value"] == 123

def test_get_dummy():
    payload = {
        "name": "Another Dummy",
        "value": 456
    }
    post_response = client.post("/dummy/", json=payload)
    created_id = post_response.json()["id"]

    get_response = client.get(f"/dummy/{created_id}")
    assert get_response.status_code == 200
    fetched_data = get_response.json()

    assert fetched_data["id"] == created_id
    assert fetched_data["item"]["name"] == "Another Dummy"
    assert fetched_data["item"]["value"] == 456

def test_get_dummy_not_found():
    response = client.get("/dummy/9999") 
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
    
def test_search_image():
    with open("./tests/KimBap.jpg", "rb") as f:
        response = client.post("/image_search/search-image", files={"file": f})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0