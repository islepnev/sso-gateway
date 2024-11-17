from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from app.auth.exceptions import RedirectToLoginException
from app.utils.config_manager import ConfigManager
from app.utils.logger import setup_logging
from app.routes import include_routes
from app.utils.url_helpers import get_login_url
from app.context_manager import app_context, initialize_context


# Initialize Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

def create_app():
    setup_logging()

    initialize_context()
    config = ConfigManager.get_config()
    app = FastAPI(
        title="SSO Gateway",
        docs_url=f"{config.gateway.prefix}/docs",
        redoc_url=f"{config.gateway.prefix}/redoc",
        )

    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    include_routes(app)

    @app.exception_handler(RedirectToLoginException)
    async def redirect_to_login_exception_handler(request: Request, exc: RedirectToLoginException):
        # Redirect to login page with `next` query parameter to store original URL
        login_url = get_login_url(exc.original_url)
        return RedirectResponse(url=login_url)

    @app.on_event("startup")
    async def startup():
        await app_context.startup()

    @app.on_event("shutdown")
    async def shutdown():
        await app_context.shutdown()

    return app

app = create_app()