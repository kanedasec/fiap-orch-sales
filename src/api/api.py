import logging
from fastapi import APIRouter, Depends, Header, HTTPException
from src.schemas.purchase import PurchaseIn, PurchaseOut
from src.usecases.purchase import purchase_vehicle
from src.api.auth import get_current_user
from src.utils.correlation import ensure_correlation_id, HEADER as CORR_HEADER

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/purchase", response_model=PurchaseOut, tags=["sales"])
async def purchase(
    body: PurchaseIn,
    user: dict = Depends(get_current_user),
    x_request_id: str | None = Header(None),
):
    corr_id = ensure_correlation_id(x_request_id)
    try:
        buyer_id = user.get("sub")  # ID do Keycloak
        return await purchase_vehicle(buyer_id, body, corr_id)
    except Exception as e:
        log.exception("purchase failed: %s", e)
        raise HTTPException(status_code=500, detail="purchase_failed")
