from dataclasses import dataclass
from typing import Optional
import yaml
from pathlib import Path


@dataclass(frozen=True)
class KeycloakConfig:
    server_url: str
    realm: str
    client_id: str
    client_secret: str
    redirect_uri: str
    username_claim: str
    verify_ssl: Optional[bool] = True  # Default to True if not specified


@dataclass(frozen=True)
class GatewayConfig:
    prefix: str = "/gateway"
    database_url: str = "sqlite:///./tokens.db"
    backend_url: str = "http://example.com"


@dataclass(frozen=True)
class AppConfig:
    keycloak: KeycloakConfig
    gateway: GatewayConfig
