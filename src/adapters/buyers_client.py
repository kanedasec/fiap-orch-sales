import httpx
from src.core.config import settings

class BuyersClient:
    def __init__(self, corr_id: str):
        self.base = settings.BUYERS_BASE_URL
        self.corr = corr_id

    def _headers(self):
        return {"Accept": "application/json", "X-Request-ID": self.corr}

    async def get_buyer(self, buyer_id: str):
        url = f"{self.base}/buyers/{buyer_id}"
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.get(url, headers=self._headers())
            r.raise_for_status()
            return r.json()
