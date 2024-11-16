from fastapi import APIRouter, Depends, Request
from app.auth.dependencies import get_current_user
from starlette.responses import RedirectResponse

from app.auth.exceptions import RedirectToLoginException
from app.utils import logger

router = APIRouter()

@router.get("/")
async def protected_route(current_user: dict = Depends(get_current_user), request: Request = None):
    if not current_user:
        logger.info(f"Unauthorized, redirecting to login page.")
        raise RedirectToLoginException(original_url=str(request.url))
    return {"message": f"Hello, {current_user.get('preferred_username')}!"}
