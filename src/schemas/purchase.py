# src/schemas/purchase.py
from pydantic import BaseModel
from uuid import UUID

class PurchaseIn(BaseModel):
    vehicle_id: UUID

class PurchaseOut(BaseModel):
    order_id: UUID
    vehicle_id: UUID
    buyer_id: UUID
    payment_id: UUID
    status: str

