import uuid
from src.adapters.buyers_client import BuyersClient
from src.adapters.vehicles_client import VehiclesClient
from src.adapters.payments_client import PaymentsClient
from src.schemas.purchase import PurchaseIn, PurchaseOut

async def purchase_vehicle(buyer_id: str, data: PurchaseIn, corr_id: str) -> PurchaseOut:
    buyers = BuyersClient(corr_id)
    vehicles = VehiclesClient(corr_id)
    payments = PaymentsClient(corr_id)

    # 1. Valida comprador
    buyer = await buyers.get_buyer(buyer_id)

    # 2. Reserva veículo
    vehicle = await vehicles.reserve_vehicle(str(data.vehicle_id))

    # 3. Processa pagamento
    payment = await payments.process_payment(buyer_id, str(data.vehicle_id), data.payment_method)

    # 4. Retorna ordem consolidada
    return PurchaseOut(
        order_id=uuid.uuid4(),
        vehicle_id=data.vehicle_id,
        buyer_id=buyer["id"],
        payment_id=payment["id"],
        status="SUCCESS"
    )
