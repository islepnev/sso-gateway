from fastapi import Request
from app.auth.keycloak import get_keycloak_openid
from app.utils.sessions import get_token, set_token
import logging

logger = logging.getLogger(__name__)

async def refresh_token_if_needed(request: Request, response):
    token = get_token(request)
    if token and token.get('expires_in') < 60:
        try:
            keycloak_openid = get_keycloak_openid()
            new_token = await keycloak_openid.refresh_token(token['refresh_token'])
            set_token(response, new_token)
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            # Optionally redirect to login
