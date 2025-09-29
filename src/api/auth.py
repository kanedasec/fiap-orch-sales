import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from src.core.config import settings

security = HTTPBearer()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Baixa JWKS do Keycloak
        jwks_url = f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as client:
            resp = await client.get(jwks_url)
            resp.raise_for_status()
            jwks = resp.json()["keys"]

        # Decodifica token
        unverified = jwt.get_unverified_header(token.credentials)
        key = next((k for k in jwks if k["kid"] == unverified["kid"]), None)
        if not key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid key")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        payload = jwt.decode(
            token.credentials,
            public_key,
            algorithms=["RS256"],
            audience=settings.KEYCLOAK_CLIENT_ID,
            options={"verify_exp": True}
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
