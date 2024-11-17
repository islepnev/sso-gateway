# app/utils/url_helpers.py

from fastapi import Request

from app.utils.config_manager import ConfigManager


def get_base_url(request: Request) -> str:
    """
    Determine the base URL based on request headers.
    - If behind a reverse proxy, use X-Forwarded-Host and X-Forwarded-Proto.
    - Otherwise, derive from the request's host and scheme.
    """
    forwarded_proto = request.headers.get("x-forwarded-proto")
    forwarded_host = request.headers.get("x-forwarded-host")
    
    if forwarded_host:
        scheme = forwarded_proto if forwarded_proto else "http"
        base_url = f"{scheme}://{forwarded_host}"
    else:
        scheme = "https" if request.url.scheme == "https" else "http"
        base_url = f"{scheme}://{request.client.host}"
    
    return base_url


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
