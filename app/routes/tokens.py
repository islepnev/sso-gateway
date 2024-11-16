from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.auth.dependencies import get_current_user
from app.utils.config_manager import ConfigManager
from app.utils.tokens import generate_token
from app.utils.database import api_tokens, get_database
from app.models.token import APIToken
from typing import List

router = APIRouter(tags=["tokens"])

@router.post("/generate", response_model=APIToken)
async def generate_api_token(current_user: dict = Depends(get_current_user)):
    token = generate_token()
    config = ConfigManager.get_config()
    user_id = current_user.get(config.keycloak.username_claim)  # Assuming 'sub' is the user ID
    query = api_tokens.insert().values(token=token, user_id=user_id)
    database = get_database()
    await database.execute(query)
    # Fetch the inserted record to get the auto-populated 'created_at'
    fetch_query = select(api_tokens).where(api_tokens.c.token == token)
    record = await database.fetch_one(fetch_query)
    return APIToken(
        token=record["token"],
        user_id=record["user_id"],
        created_at=record["created_at"]
    )


@router.get("/", response_model=List[APIToken])
async def list_api_tokens(current_user: dict = Depends(get_current_user)):
    config = ConfigManager.get_config()
    user_id = current_user.get(config.keycloak.username_claim)
    query = api_tokens.select().where(api_tokens.c.user_id == user_id)
    database = get_database()
    rows = await database.fetch_all(query)
    return [APIToken(**row) for row in rows]

@router.delete("/revoke/{token}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_token(token: str, current_user: dict = Depends(get_current_user)):
    config = ConfigManager.get_config()
    user_id = current_user.get(config.keycloak.username_claim)
    query = api_tokens.delete().where(api_tokens.c.token == token, api_tokens.c.user_id == user_id)
    database = get_database()
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Token not found")
