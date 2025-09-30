import uuid
from fastapi import HTTPException
from src.adapters.buyers_client import BuyersClient
from src.adapters.vehicles_client import VehiclesClient
from src.adapters.payments_client import PaymentsClient
from src.schemas.purchase import PurchaseIn, PurchaseOut

async def purchase_vehicle(user_sub: str, data: PurchaseIn, corr_id: str) -> PurchaseOut:
    buyers = BuyersClient(corr_id)
    vehicles = VehiclesClient(corr_id)
    payments = PaymentsClient(corr_id)

    # 1. Resolve comprador pelo external_id (sub do Keycloak)
    buyer = await buyers.get_buyer_by_external_id(user_sub)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    buyer_id = buyer["id"]

    # 2. Reserva veículo (retorna também preço)
    vehicle = await vehicles.reserve_vehicle(str(data.vehicle_id), buyer_id)

    # 3. Processa pagamento com o preço do veículo
    payment = await payments.process_payment(
        buyer_id=buyer_id,
        vehicle_id=str(data.vehicle_id),
        amount=vehicle["price"]
    )
    payment_id = payment["id"]

    # 4. 🔄 Mock: aprova pagamento imediatamente
    approved_payment = await payments.update_payment_status(payment_id, "APPROVED")

    # 5. 🔄 Mock: marca veículo como vendido
    sold_vehicle = await vehicles.sell_vehicle(str(data.vehicle_id))

    # 6. Retorna ordem consolidada
    return PurchaseOut(
        order_id=uuid.uuid4(),
        vehicle_id=data.vehicle_id,
        buyer_id=buyer_id,
        payment_id=payment_id,
        status="SUCCESS"
    )
