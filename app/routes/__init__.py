# app/routes/__init__.py

from fastapi import APIRouter, FastAPI

from app.utils.config_manager import ConfigManager

from .api import router as backend_proxy_router
from .auth import router as auth_router
from .protected import router as protected_router
from .error import router as error_router
from .tokens import router as tokens_router
from .home import router as home_router  # Import the home router


def include_routes(app: FastAPI):
    """
    Dynamically include routers with prefixes derived from the configuration.
    """
    config = ConfigManager.get_config()
    gateway_prefix = config.gateway.prefix

    # Create gateway router with dynamic prefix
    gateway_router = APIRouter(prefix=gateway_prefix)

    # Include modular routes
    gateway_router.include_router(auth_router, prefix="/auth")
    gateway_router.include_router(protected_router, prefix="/protected")
    gateway_router.include_router(error_router, prefix="/error")
    gateway_router.include_router(tokens_router, prefix="/tokens")
    gateway_router.include_router(home_router, prefix="")

    # Include gateway routes
    app.include_router(gateway_router)

    # Include API router without the gateway prefix
    api_router = APIRouter()
    api_router.include_router(backend_proxy_router, prefix="/api", include_in_schema=False)
    app.include_router(api_router)
