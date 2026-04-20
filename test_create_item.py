import allure
import pytest
from utils.data_generator import generate_seller_id, generate_item_name, generate_price, generate_statistics

@allure.feature("Создание объявления")
class TestCreateItem:
    @allure.title("Успешное создание объявления с валидными данными")
    @pytest.mark.xfail(reason="BUG-003: API требует поле likes на верхнем уровне")
    def test_create_valid_item(self, client, unique_seller_id):
        stats = generate_statistics(likes=0, view_count=0, contacts=0)
        resp = client.create_item(unique_seller_id, "Test Item", 10000, stats)
        assert resp["status_code"] == 200

    @allure.title("Создание объявления со всеми полями статистики")
    @pytest.mark.xfail(reason="BUG-003: API требует поле likes на верхнем уровне")
    def test_create_item_with_statistics(self, client, unique_seller_id):
        stats = generate_statistics(likes=10, view_count=100, contacts=5)
        resp = client.create_item(unique_seller_id, "Item with stats", 5000, stats)
        assert resp["status_code"] == 200

    @allure.title("Создание объявления с отрицательной ценой")
    def test_create_item_negative_price(self, client, unique_seller_id):
        stats = generate_statistics()
        resp = client.create_item(unique_seller_id, "Negative price", -100, stats)
        assert resp["status_code"] == 400

    @allure.title("Создание объявления с нулевой ценой")
    def test_create_item_zero_price(self, client, unique_seller_id):
        stats = generate_statistics()
        resp = client.create_item(unique_seller_id, "Zero price", 0, stats)
        assert resp["status_code"] == 400

    @allure.title("Создание объявления с пустым названием")
    def test_create_item_empty_name(self, client, unique_seller_id):
        stats = generate_statistics()
        resp = client.create_item(unique_seller_id, "", 1000, stats)
        assert resp["status_code"] == 400

    @allure.title("Создание объявления без sellerID")
    def test_create_item_without_seller_id(self, client):
        stats = generate_statistics()
        resp = client.session.post(
            f"{client.base_url}/api/1/item",
            json={"name": "No seller", "price": 1000, "statistics": stats}
        )
        assert resp.status_code == 400

    @allure.title("Создание объявления с невалидным sellerID")
    def test_create_item_invalid_seller_id_type(self, client):
        stats = generate_statistics()
        resp = client.create_item("not_a_number", "Item", 1000, stats)
        assert resp["status_code"] == 400