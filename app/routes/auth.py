import logging
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from app.auth.keycloak import get_keycloak_openid
from app.utils.config_manager import ConfigManager
import urllib.parse
from app.utils import sessions

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/login")
async def login(request: Request):
    config = ConfigManager.get_config()
    original_url = request.query_params.get("next", "/protected")  # Default to /protected
    state = original_url  # Include original URL in state
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
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    redirect_uri = request.url_for('callback')

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
        original_url = state if state else "/protected"  # Fallback if state is missing
        response = RedirectResponse(url=original_url)
        sessions.set_token(response, session_data)
        return response
    except Exception as e:
        logger.error(f"Error during callback: {e}")
        return RedirectResponse(url='/error')


@router.get("/logout")
async def logout(request: Request):
    token = sessions.get_token(request)
    if token:
        try:
            keycloak_openid = get_keycloak_openid()
            await keycloak_openid.logout(token['refresh_token'])
        except Exception as e:
            logger.error(f"Error during logout: {e}")
    response = RedirectResponse(url='/')
    sessions.clear_token(response)
    return response
