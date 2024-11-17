import logging
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from starlette.datastructures import URL
from app.auth.keycloak import get_keycloak_openid
from app.utils.config_manager import ConfigManager
import urllib.parse
from app.utils import sessions

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/login")
async def login(request: Request):
    config = ConfigManager.get_config()
    # external_url = request.url.replace(host=request.headers.get("host"))
    host = request.headers.get("host")
    original_url = request.query_params.get("next")  # Use `next` if provided
    if not original_url:
        # Reconstruct the current URL with the external host if `next` is not provided
        url = URL(str(request.url))  # Parse request.url into a URL object
        original_url = str(url.replace(netloc=host))  # Replace the netloc with the external host

    state = urllib.parse.quote(original_url) # urllib.parse.urlencode({"next": original_url})
    redirect_uri = config.keycloak.redirect_uri
    try:
        keycloak_openid = get_keycloak_openid()
        auth_url = await keycloak_openid.auth_url(redirect_uri=redirect_uri, state=state, scope="email openid")
        return RedirectResponse(auth_url)
    except Exception as e:
        logger.error(f"Error generating auth URL: {e}")
        error_url = str(request.url_for("error"))
        return RedirectResponse(url=error_url)

@router.get("/callback")
async def callback(request: Request):
    config = ConfigManager.get_config()
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    redirect_uri = config.keycloak.redirect_uri # request.url_for('callback')

    try:
        keycloak_openid = get_keycloak_openid()
        token = await keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri=redirect_uri
        )

        # Fetch userinfo and store it along with the token
        userinfo = await keycloak_openid.userinfo(token['access_token'])
        session_data = {"token": token, "userinfo": userinfo}

        # Save the token in session (or cookie)
        original_url = urllib.parse.unquote(state) if state else "/protected"
        response = RedirectResponse(url=original_url)
        sessions.set_token(response, session_data)
        return response
    except Exception as e:
        logger.error(f"Error during callback: {e}")
        error_url = str(request.url_for("error"))
        return RedirectResponse(error_url)


@router.get("/logout")
async def logout(request: Request):
    config = ConfigManager.get_config()
    next_url = request.query_params.get("next", f"{config.gateway.prefix}/")
    token = sessions.get_token(request)
    if token and "refresh_token" in token:
        try:
            keycloak_openid = get_keycloak_openid()
            await keycloak_openid.logout(token['refresh_token'])
        except Exception as e:
            logger.error(f"Error during logout: {e}")
    response = RedirectResponse(url=next_url)
    sessions.clear_token(response)
    return response
