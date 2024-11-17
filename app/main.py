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
        description=(
            "The SSO Gateway simplifies secure access to backend services by providing "
            "authentication and token management while transparently proxying requests."
        ),
        summary="A lightweight SSO integration and API proxy for backend services.",
        terms_of_service="https://github.com/islepnev/sso-gateway/blob/master/TERMS.md",
        contact={
            "name": "SSO Gateway Maintainers",
            "url": "https://github.com/islepnev/sso-gateway",
            # "email": "islepnev@jinr.int"
        },
        license_info={
            "name": "GNU General Public License v3.0",
            "url": "https://www.gnu.org/licenses/gpl-3.0.html"
        },
        docs_url=f"{config.gateway.prefix}/docs",
        redoc_url=f"{config.gateway.prefix}/redoc",
        openapi_url=f"{config.gateway.prefix}/openapi.json",
        )

    # Mount static files
    app.mount(f"{config.gateway.prefix}/static", StaticFiles(directory="app/static"), name="static")

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
