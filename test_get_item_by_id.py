import allure
from utils.data_generator import generate_invalid_id

@allure.feature("Получение объявления по ID")
class TestGetItemById:
    @allure.title("Получение существующего объявления")
    def test_get_existing_item(self, client, created_item):
        resp = client.get_item_by_id(created_item["id"])
        assert resp["status_code"] == 200

    @allure.title("Получение несуществующего объявления")
    def test_get_non_existent_item(self, client):
        resp = client.get_item_by_id(generate_invalid_id())
        assert resp["status_code"] == 404

    @allure.title("Получение объявления с пустым ID")
    def test_get_item_empty_id(self, client):
        resp = client.get_item_by_id("")
        assert resp["status_code"] in [400, 404]

    @allure.title("Получение объявления после удаления")
    def test_get_deleted_item(self, client, created_item):
        client.delete_item_v2(created_item["id"])
        resp = client.get_item_by_id(created_item["id"])
        assert resp["status_code"] == 404