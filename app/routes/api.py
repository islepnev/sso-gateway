from fastapi import APIRouter, Depends
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import Response
import httpx
from app.auth.token_dependencies import validate_api_token
from app.utils.config_manager import ConfigManager

router = APIRouter()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_api(
    path: str,
    request: Request,
    user_id: str = Depends(validate_api_token),  # Validate API token
):
    """
    Proxy requests to the backend app at the /api endpoint.
    """

    # Retrieve the backend URL from the configuration
    config = ConfigManager.get_config()
    backend_url = f"{config.gateway.backend_url}/{path}"

    # Prepare request to the backend
    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in ["host", "authorization"]
    }
    headers["X-Remote-User"] = user_id

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=backend_url,
                headers=headers,
                content=await request.body()
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error proxying request: {e}")
