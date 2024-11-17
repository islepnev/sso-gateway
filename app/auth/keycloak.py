import logging
from app.context_manager import app_context

logger = logging.getLogger(__name__)

def get_keycloak_openid():
    return app_context.keycloak_openid


async def get_user_info(access_token: str):
    try:
        keycloak_openid = get_keycloak_openid()
        userinfo = await keycloak_openid.userinfo(access_token)
        return userinfo
    except Exception as e:
        logger.error(f"Failed to get user info: {e}")
        return None
