import logging
from sqlite3 import OperationalError
from fastapi import APIRouter, Depends, Request
from fastapi.routing import APIRoute
from starlette.templating import Jinja2Templates
from app.auth.dependencies import get_current_user_id
from app.context_manager import app_context
from app.utils.config_manager import ConfigManager

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", include_in_schema=False)
async def home(
    request: Request,
        user_id: str = Depends(get_current_user_id),
    ):
    config = ConfigManager.get_config()
    gateway_prefix = config.gateway.prefix

    # Fetch version from app metadata
    version = request.app.openapi()["info"]["version"]

    # Fetch tokens
    query = """
        SELECT api_tokens.token, api_tokens.created_at, api_tokens.user_id
        FROM api_tokens
    """
    try:
        tokens = await app_context.database.fetch_all(query)
    except OperationalError as e:
        logging.error(f"Database error: {e}")
        tokens = []

    # Collect all routes under the gateway prefix
    routes = []
    for route in request.app.routes:
        if isinstance(route, APIRoute):
            path = route.path
            # Exclude OpenAPI and static routes
            if route.path in ["/openapi.json", "/docs", "/redoc", "/static/{path:path}"]:
                continue
            # Prepend gateway prefix if the route is part of the gateway
            if not route.path.startswith(gateway_prefix):
                prefixed_path = f"{gateway_prefix}{route.path}"
            else:
                prefixed_path = route.path

            routes.append({
                "path": prefixed_path,
                "methods": ",".join(route.methods),
            })

    response = templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "routes": routes,
            "tokens": tokens,
            "gateway_prefix": gateway_prefix,
            "version": version,
            "user_id": user_id,
            "is_authenticated": user_id is not None,
        },
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
