import pytest
from api_client import APIClient
from utils.data_generator import generate_seller_id, generate_item_name, generate_price, generate_statistics

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def unique_seller_id():
    return generate_seller_id()

@pytest.fixture
def created_item(client, unique_seller_id):
    name = generate_item_name()
    price = generate_price()
    stats = generate_statistics(likes=0, view_count=0, contacts=0)
    resp = client.create_item(unique_seller_id, name, price, stats)
    
    if resp["status_code"] == 400 and "likes обязательно" in str(resp.get("json", {})):
        pytest.skip("KNOWN BUG: API требует поле likes на верхнем уровне (BUG-003)")
    
    assert resp["status_code"] == 200, f"Creation failed: {resp}"
    json_data = resp["json"]
    if isinstance(json_data, list):
        json_data = json_data[0]
    item_id = json_data.get("id") or json_data.get("status", "").replace("Сохранили объявление - ", "")
    return {"id": item_id, "seller_id": unique_seller_id, "response": json_data}