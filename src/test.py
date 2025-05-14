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
    assert response.json()["message"] == "Item not found"
    
def test_search_image():
    with TestClient(app) as client:
        with open("./tests/KimBap.jpg", "rb") as f:
            response = client.post("/image-search", files={"file": f})
        assert response.status_code == 200
        data = response.json()
        assert len(data['data']) > 0

def test_valid_restaurant_id():
    restaurant_id = "1bb6891b-b737-4de9-a98a-444178854e8e"
    response = client.get(f"restaurant/{restaurant_id}")
    assert response.status_code == 200
    data = response.json()
    assert "restaurant_id" in data["data"]
    assert data["data"]["restaurant_id"] == restaurant_id
    assert data["data"]["restaurant_name"] == "3A Korean Food - Gà Sốt Phô Mai, Mì Cay Hàn Quốc & Tokbokki - Nguyễn Văn Luông"

def test_valid_restaurant_dishes():
    restaurant_id = "1bb6891b-b737-4de9-a98a-444178854e8e"
    response = client.get(f"restaurant/{restaurant_id}/dishes?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "metadata" in data
    assert "page" in data["metadata"]
    assert "size" in data["metadata"]
    assert "total" in data["metadata"]


def test_valid_restaurant_reviews():
    restaurant_id = "1bb6891b-b737-4de9-a98a-444178854e8e"
    response = client.get(f"restaurant/{restaurant_id}/reviews?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "metadata" in data
    assert "page" in data["metadata"]
    assert "size" in data["metadata"]
    assert "total" in data["metadata"]
    
def test_valid_collaborative_filtering():
    user_id = "bf12d0ce-11bd-407e-abb1-e9cbba669232"
    response = client.get(f"recommendation/user/{user_id}?top_n=20")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "score" in data["data"][0]
    assert "restaurant_id" in data["data"][0]

def test_valid_random_recommendation():
    response = client.get(f"recommendation/guest")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "restaurant_id" in data["data"][0]

def test_get_dish():
    valid_img_id = "3d665b19-5cf6-4590-85ce-4c1596b997aa"
    response = client.get(f"/dish/{valid_img_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert "status" in response_data
    assert response_data["status"] == 200
    assert "data" in response_data
    assert isinstance(response_data["data"], dict) 
    assert "img_id" in response_data["data"]
    assert response_data["data"]["img_id"] == str(valid_img_id)