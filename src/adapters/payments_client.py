import httpx
from src.core.config import settings

class PaymentsClient:
    def __init__(self, corr_id: str):
        self.base = settings.PAYMENTS_BASE_URL
        self.corr = corr_id

    def _headers(self):
        return {"Accept": "application/json", "X-Request-ID": self.corr}

    async def process_payment(self, buyer_id: str, vehicle_id: str, amount: float):
        url = f"{self.base}/payments"
        payload = {
            "buyer_id": buyer_id,
            "vehicle_id": vehicle_id,
            "amount": amount
        }
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.post(url, json=payload, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def update_payment_status(self, payment_id: str, status: str):
        url = f"{self.base}/payments/{payment_id}"
        payload = {"status": status}  # garantir lowercase
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.patch(url, json=payload, headers=self._headers())
            r.raise_for_status()
            return r.json()

