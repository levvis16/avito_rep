import allure
from utils.data_generator import generate_invalid_id, generate_statistics

@allure.feature("Получение статистики по объявлению")
class TestGetStatistics:
    @allure.title("Получение статистики существующего объявления")
    def test_get_statistics(self, client, created_item):
        resp = client.get_statistic(created_item["id"])
        assert resp["status_code"] == 200

    @allure.title("Получение статистики несуществующего объявления")
    def test_get_statistics_non_existent(self, client):
        resp = client.get_statistic(generate_invalid_id())
        assert resp["status_code"] == 404

    @allure.title("Получение статистики с заданными значениями")
    def test_get_statistics_with_values(self, client, unique_seller_id):
        stats = generate_statistics(likes=42, view_count=1337, contacts=7)
        create_resp = client.create_item(unique_seller_id, "Stats item", 9999, stats)
        assert create_resp["status_code"] == 200
        json_data = create_resp["json"]
        if isinstance(json_data, list):
            json_data = json_data[0]
        item_id = json_data.get("id") or json_data.get("status", "").replace("Сохранили объявление - ", "")
        resp = client.get_statistic(item_id)
        assert resp["status_code"] == 200

    @allure.title("Сравнение статистики v1 и v2")
    def test_statistics_v1_v2_consistency(self, client, created_item):
        resp_v1 = client.get_statistic(created_item["id"])
        resp_v2 = client.get_statistic_v2(created_item["id"])
        assert resp_v1["status_code"] == resp_v2["status_code"]