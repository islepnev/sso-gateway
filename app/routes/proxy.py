from fastapi import APIRouter, Depends, Request
from starlette.responses import Response
from app.auth.token_dependencies import validate_api_token
import httpx
from app.utils.config_manager import ConfigManager

router = APIRouter()

@router.api_route("/netdisco/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_netdisco(path: str, request: Request, user_id: str = Depends(validate_api_token)):
    async with httpx.AsyncClient() as client:
        # Construct the full URL
        config = ConfigManager.get_config()
        url = f"{config.gateway.backend_url}/{path}"
        
        # Prepare headers, including X-Remote-User
        headers = dict(request.headers)
        headers["X-Remote-User"] = user_id
        
        # Forward the request to NetDisco
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=await request.body()
        )
        
        # Return the response from NetDisco
        return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
