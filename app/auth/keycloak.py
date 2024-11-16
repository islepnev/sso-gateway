import logging
from keycloak import KeycloakOpenID
from app.utils.config_manager import ConfigManager
from app.context_manager import app_context

logger = logging.getLogger(__name__)

def get_keycloak_openid():
    return app_context.keycloak_openid

# # Lazy initialization of KeycloakOpenID
# _keycloak_openid = None


# def get_keycloak_openid() -> KeycloakOpenID:
#     """
#     Lazily initialize and return the KeycloakOpenID instance.
#     Ensures configuration is loaded before initialization.
#     """
#     global _keycloak_openid
#     if _keycloak_openid is None:
#         config = ConfigManager.get_config()
#         try:
#             _keycloak_openid = KeycloakOpenID(
#                 server_url=config.keycloak.server_url,
#                 realm_name=config.keycloak.realm,
#                 client_id=config.keycloak.client_id,
#                 client_secret_key=config.keycloak.client_secret,
#                 verify=config.keycloak.verify_ssl,
#             )
#             logger.info("KeycloakOpenID initialized successfully.")
#         except Exception as e:
#             logger.error(f"Failed to initialize KeycloakOpenID: {e}")
#             raise
#     return _keycloak_openid


async def get_user_info(access_token: str):
    try:
        keycloak_openid = get_keycloak_openid()
        userinfo = await keycloak_openid.userinfo(access_token)
        return userinfo
    except Exception as e:
        logger.error(f"Failed to get user info: {e}")
        return None
