from starlette.requests import Request
from starlette.responses import Response
from app.context_manager import app_context

TOKEN_COOKIE_NAME = 'auth_token'


def set_token(response: Response, session_data: dict):
    serializer = app_context.serializer
    token_serialized = serializer.dumps(session_data)
    response.set_cookie(TOKEN_COOKIE_NAME, token_serialized, httponly=True, max_age=3600)

def get_token(request: Request):
    token_serialized = request.cookies.get(TOKEN_COOKIE_NAME)
    if token_serialized:
        try:
            serializer = app_context.serializer
            session_data = serializer.loads(token_serialized, max_age=3600)
            return session_data
        except Exception:
            return None
    return None

def clear_token(response: Response):
    response.delete_cookie(TOKEN_COOKIE_NAME)
