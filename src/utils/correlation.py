import uuid
from fastapi import Header

HEADER = "X-Request-ID"

def ensure_correlation_id(x_request_id: str | None = None) -> str:
    return x_request_id or str(uuid.uuid4())
