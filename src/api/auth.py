import httpx
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from src.core.config import settings

log = logging.getLogger(__name__)
security = HTTPBearer()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # 🔑 Baixa JWKS do Keycloak
        jwks_url = f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECS) as client:
            resp = await client.get(jwks_url)
            resp.raise_for_status()
            jwks = resp.json()["keys"]

        # 🔍 Pega chave correta pelo "kid" do token
        unverified = jwt.get_unverified_header(token.credentials)
        key = next((k for k in jwks if k["kid"] == unverified["kid"]), None)
        if not key:
            log.error("❌ JWKS key not found for kid=%s", unverified["kid"])
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid key")

        # ✅ Decodifica com o JWK diretamente
        payload = jwt.decode(
            token.credentials,
            key,  # python-jose aceita JWK direto
            algorithms=["RS256"],
            options={"verify_exp": True, "verify_aud": False}
        )

        # Validação extra de aud/azp
        aud = payload.get("aud")
        azp = payload.get("azp")

        valid_aud = aud == "account" or (isinstance(aud, list) and "account" in aud)
        valid_azp = azp == settings.KEYCLOAK_CLIENT_ID

        if not (valid_aud and valid_azp):
            log.error("❌ Invalid token audience or client: aud=%s azp=%s", aud, azp)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid audience/client")

        log.info("✅ Token valid for sub=%s, client=%s", payload.get("sub"), azp)
        return payload

    except Exception as e:
        log.error("❌ Token validation failed: %s", e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
