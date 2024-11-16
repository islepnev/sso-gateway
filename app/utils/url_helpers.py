from app.utils.config_manager import ConfigManager
from app.routes.auth import router as auth_router


def get_login_url(next: str) -> str:
    """
    Dynamically construct the login URL using configuration and router prefix.
    """
    config = ConfigManager.get_config()
    gateway_path = config.gateway.prefix.rstrip("/")  # Ensure no trailing slash
    auth_prefix = 'auth' # auth_router.prefix.lstrip("/")  # Remove leading slash if present
    login_path = "login"
    next = f"?next={next}" if next else ""
    url = f"{gateway_path}/{auth_prefix}/{login_path}{next}"
    return url
