import os
import requests


class TeslaFleetAPI:
    """Simple wrapper for the Tesla Fleet API."""

    def __init__(self, base_url=None, token=None):
        self.base_url = (
            base_url.rstrip("/")
            if base_url
            else "https://fleet-api.prd.na.vn.cloud.tesla.com"
        )
        if token is None:
            token = os.getenv("FLEET_API_TOKEN")
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _get(self, path):
        url = f"{self.base_url}{path}"
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def _post(self, path, json=None):
        url = f"{self.base_url}{path}"
        r = self.session.post(url, json=json)
        r.raise_for_status()
        return r.json()

    def vehicle_list(self):
        data = self._get("/api/1/vehicles")
        return data.get("response", [])

    def vehicle_data(self, vehicle_id):
        data = self._get(f"/api/1/vehicles/{vehicle_id}/vehicle_data")
        return data.get("response", {})

    def wake_up(self, vehicle_id):
        data = self._post(f"/api/1/vehicles/{vehicle_id}/wake_up")
        return data.get("response", {})
