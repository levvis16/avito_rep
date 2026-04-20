import allure
import pytest
from utils.data_generator import generate_seller_id, generate_statistics

@allure.feature("E2E сценарии")
class TestE2E:
    @pytest.mark.xfail(reason="BUG-003: API требует поле likes на верхнем уровне")
    def test_full_item_lifecycle(self, client):
        seller_id = generate_seller_id()
        stats = generate_statistics()
        with allure.step("Создание объявления"):
            create_resp = client.create_item(seller_id, "E2E Item", 7777, stats)
            assert create_resp["status_code"] == 200
            json_data = create_resp["json"]
            if isinstance(json_data, list):
                json_data = json_data[0]
            item_id = json_data.get("id") or json_data.get("status", "").replace("Сохранили объявление - ", "")
        with allure.step("Получение объявления по ID"):
            get_resp = client.get_item_by_id(item_id)
            assert get_resp["status_code"] == 200
        with allure.step("Получение объявлений продавца"):
            seller_resp = client.get_items_by_seller(seller_id)
            assert seller_resp["status_code"] == 200
        with allure.step("Удаление объявления"):
            del_resp = client.delete_item_v2(item_id)
            assert del_resp["status_code"] == 200
        with allure.step("Проверка что объявление удалено"):
            get_deleted = client.get_item_by_id(item_id)
            assert get_deleted["status_code"] == 404

    @pytest.mark.xfail(reason="BUG-003: API требует поле likes на верхнем уровне")
    def test_multiple_items_creation(self, client):
        seller_id = generate_seller_id()
        stats = generate_statistics()
        created_ids = []
        for i in range(3):
            resp = client.create_item(seller_id, f"Item {i}", 1000 + i * 100, stats)
            assert resp["status_code"] == 200
            json_data = resp["json"]
            if isinstance(json_data, list):
                json_data = json_data[0]
            item_id = json_data.get("id") or json_data.get("status", "").replace("Сохранили объявление - ", "")
            created_ids.append(item_id)
        seller_items = client.get_items_by_seller(seller_id)
        assert seller_items["status_code"] == 200
        for item_id in created_ids:
            client.delete_item_v2(item_id)

    @pytest.mark.xfail(reason="BUG-003: API требует поле likes на верхнем уровне")
    def test_idempotency_create(self, client, unique_seller_id):
        stats = generate_statistics()
        resp1 = client.create_item(unique_seller_id, "Idempotent item", 5555, stats)
        resp2 = client.create_item(unique_seller_id, "Idempotent item", 5555, stats)
        assert resp1["status_code"] == 200
        assert resp2["status_code"] == 200
        json1 = resp1["json"]
        json2 = resp2["json"]
        if isinstance(json1, list):
            json1 = json1[0]
        if isinstance(json2, list):
            json2 = json2[0]
        id1 = json1.get("id") or json1.get("status", "").replace("Сохранили объявление - ", "")
        id2 = json2.get("id") or json2.get("status", "").replace("Сохранили объявление - ", "")
        assert id1 != id2