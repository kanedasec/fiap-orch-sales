import httpx
from src.core.config import settings

class VehiclesClient:
    def __init__(self, corr_id: str):
        self.base = settings.VEHICLES_BASE_URL
        self.corr = corr_id

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "X-Request-ID": self.corr
        }

    async def reserve_vehicle(self, vehicle_id: str, buyer_id: str):
        """
        Reserva um veículo associando-o a um comprador.
        Envia { "reserved_by": <buyer_id> } para o serviço de veículos.
        """
        url = f"{self.base}/vehicles/{vehicle_id}/reserve"
        payload = {"reserved_by": buyer_id}

        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.post(url, json=payload, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def unreserve_vehicle(self, vehicle_id: str):
        """
        Remove a reserva de um veículo.
        """
        url = f"{self.base}/vehicles/{vehicle_id}/unreserve"
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.post(url, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def sell_vehicle(self, vehicle_id: str):
        url = f"{self.base}/vehicles/{vehicle_id}/sell"
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as c:
            r = await c.post(url, headers=self._headers())
            r.raise_for_status()
            return r.json()

