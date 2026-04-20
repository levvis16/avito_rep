import requests
import config

class APIClient:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def create_item(self, seller_id, name, price, statistics=None):
        if statistics is None:
            statistics = {"likes": 0, "viewCount": 0, "contacts": 0}
        
        payload = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": statistics
        }
        response = self.session.post(f"{self.base_url}{config.CREATE_ITEM}", json=payload)
        try:
            return {"status_code": response.status_code, "json": response.json()}
        except:
            return {"status_code": response.status_code, "json": {}}

    def get_item_by_id(self, item_id):
        response = self.session.get(f"{self.base_url}{config.GET_ITEM.format(item_id)}")
        try:
            return {"status_code": response.status_code, "json": response.json()}
        except:
            return {"status_code": response.status_code, "json": {}}

    def get_items_by_seller(self, seller_id):
        response = self.session.get(f"{self.base_url}{config.GET_ITEMS_BY_SELLER.format(seller_id)}")
        try:
            return {"status_code": response.status_code, "json": response.json()}
        except:
            return {"status_code": response.status_code, "json": {}}

    def get_statistic(self, item_id):
        response = self.session.get(f"{self.base_url}{config.GET_STATISTIC.format(item_id)}")
        try:
            return {"status_code": response.status_code, "json": response.json()}
        except:
            return {"status_code": response.status_code, "json": {}}

    def delete_item_v2(self, item_id):
        response = self.session.delete(f"{self.base_url}{config.DELETE_ITEM_V2.format(item_id)}")
        try:
            return {"status_code": response.status_code, "json": response.json()}
        except:
            return {"status_code": response.status_code, "json": {}}

    def get_statistic_v2(self, item_id):
        response = self.session.get(f"{self.base_url}{config.GET_STATISTIC_V2.format(item_id)}")
        try:
            return {"status_code": response.status_code, "json": response.json()}
        except:
            return {"status_code": response.status_code, "json": {}}