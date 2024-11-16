from fastapi import Depends, HTTPException, status, Header
from app.utils.database import api_tokens, get_database
from app.models.token import APIToken

async def validate_api_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    token = authorization.split(" ")[1]
    query = api_tokens.select().where(api_tokens.c.token == token)
    database = get_database()
    token_record = await database.fetch_one(query)
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return token_record["user_id"]
