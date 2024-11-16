from fastapi import Depends, HTTPException, status, Request
from starlette.responses import RedirectResponse
from app.auth.exceptions import RedirectToLoginException
from app.utils.config_manager import ConfigManager
from app.utils.sessions import TOKEN_COOKIE_NAME, get_token, set_token
from app.auth.keycloak import get_keycloak_openid
import logging

logger = logging.getLogger(__name__)


async def get_current_user(request: Request):
    session_data = get_token(request)
    if not session_data:
        logging.debug(f"No {TOKEN_COOKIE_NAME} cookie, redirecting to login")
        raise RedirectToLoginException(original_url=str(request.url))

    try:
        # Check if userinfo is present in the session
        userinfo = session_data.get("userinfo")
        if userinfo:
            return userinfo

        keycloak_openid = get_keycloak_openid()
        token = session_data["token"]
        userinfo = await keycloak_openid.userinfo(token["access_token"])

        # Update session with fetched userinfo
        session_data["userinfo"] = userinfo
        response = RedirectResponse(url=str(request.url))
        set_token(response, session_data)
        return userinfo

    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        raise RedirectToLoginException(original_url=str(request.url))


async def get_current_user_id(request: Request) -> str:
    """
    Extract and validate the current user's ID from the session token.
    """
    session_data = get_token(request)
    if not session_data:
        return None
    userinfo = session_data.get("userinfo")
    if not userinfo:
        return None
    config = ConfigManager.get_config()
    
    return userinfo.get(config.keycloak.username_claim)

    return session_data.get("user_id")