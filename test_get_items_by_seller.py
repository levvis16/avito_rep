import allure
import pytest
from utils.data_generator import generate_seller_id, generate_statistics

@allure.feature("Получение объявлений по sellerID")
class TestGetItemsBySeller:
    @allure.title("Получение объявлений существующего продавца")
    def test_get_items_by_seller(self, client, created_item):
        resp = client.get_items_by_seller(created_item["seller_id"])
        assert resp["status_code"] == 200

    @allure.title("Получение объявлений продавца без объявлений")
    def test_get_items_by_seller_no_items(self, client):
        new_seller = generate_seller_id()
        resp = client.get_items_by_seller(new_seller)
        assert resp["status_code"] == 200

    @allure.title("Получение объявлений с невалидным sellerID")
    def test_get_items_invalid_seller_id(self, client):
        resp = client.get_items_by_seller("invalid")
        assert resp["status_code"] == 400

    @allure.title("Получение нескольких объявлений одного продавца")
    @pytest.mark.xfail(reason="BUG-003: API требует поле likes на верхнем уровне")
    def test_get_multiple_items_by_seller(self, client, unique_seller_id):
        stats = generate_statistics()
        item1 = client.create_item(unique_seller_id, "Item 1", 1000, stats)
        item2 = client.create_item(unique_seller_id, "Item 2", 2000, stats)
        assert item1["status_code"] == 200
        assert item2["status_code"] == 200