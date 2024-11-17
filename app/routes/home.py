import logging
from sqlite3 import OperationalError
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.templating import Jinja2Templates
from app.auth.dependencies import get_current_user_id
from app.context_manager import app_context
from app.utils.config_manager import ConfigManager

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


async def get_tokens():
    """Fetch API tokens from the database."""
    query = """
        SELECT api_tokens.token, api_tokens.created_at, api_tokens.user_id
        FROM api_tokens
    """
    try:
        return await app_context.database.fetch_all(query)
    except OperationalError as e:
        logging.error(f"Database error: {e}")
        return []


async def get_routes(request: Request) -> list:
    """Fetch available routes under the gateway prefix."""
    config = ConfigManager.get_config()
    gateway_prefix = config.gateway.prefix
    routes = []

    for route in request.app.routes:
        if route.path in ["/openapi.json", "/docs", "/redoc", "/static/{path:path}"]:
            continue
        if not route.path.startswith(gateway_prefix):
            path = f"{gateway_prefix}{route.path}"
        else:
            path = route.path
        if isinstance(route, APIRoute):
            routes.append({
                "path": path,
                "methods": ",".join(route.methods),
            })

    return routes


@router.get("/", include_in_schema=False)
async def home(
    request: Request,
        user_id: str = Depends(get_current_user_id),
    ):
    openapi_info = request.app.openapi().get("info", {})
    tokens = await get_tokens()
    routes = await get_routes(request)

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(openapi_info)
        
    config = ConfigManager.get_config()
    gateway_prefix = config.gateway.prefix


    response = templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "routes": routes,
            "tokens": tokens,
            "gateway_prefix": gateway_prefix,
            "openapi_info": openapi_info,
            "user_id": user_id,
            "is_authenticated": user_id is not None,
        },
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
