import httpx
from src.core.config import settings

class VehiclesClient:
    def __init__(self, corr_id: str):
        self.base = settings.VEHICLES_BASE_URL
        self.corr = corr_id

    def _headers(self):
        return {"Accept": "application/json", "X-Request-ID": self.corr}

    async def reserve_vehicle(self, vehicle_id: str):
        url = f"{self.base}/vehicles/{vehicle_id}/reserve"
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.post(url, headers=self._headers())
            r.raise_for_status()
            return r.json()
