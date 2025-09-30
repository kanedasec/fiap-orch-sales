import os

class Settings:
    PROJECT_NAME: str = "fiap-orch-sales"

    # Serviços dependentes
    BUYERS_BASE_URL: str = os.getenv("BUYERS_BASE_URL", "http://fiap-srv-buyers:8002")
    VEHICLES_BASE_URL: str = os.getenv("VEHICLES_BASE_URL", "http://fiap-srv-vehicles:8000")
    PAYMENTS_BASE_URL: str = os.getenv("PAYMENTS_BASE_URL", "http://fiap-srv-payment:8003")

    # Keycloak
    KEYCLOAK_BASE_URL: str = os.getenv("KEYCLOAK_BASE_URL", "http://keycloak:8080")
    KEYCLOAK_REALM: str = os.getenv("KEYCLOAK_REALM", "fiap-realm")
    KEYCLOAK_CLIENT_ID: str = os.getenv("KEYCLOAK_CLIENT_ID", "fiap-orch-client")
    KEYCLOAK_CLIENT_SECRET: str = os.getenv("KEYCLOAK_CLIENT_SECRET", "super-secret")

    HTTP_TIMEOUT_SECS: int = int(os.getenv("HTTP_TIMEOUT_SECS", "10"))

settings = Settings()
