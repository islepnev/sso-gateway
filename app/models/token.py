from pydantic import BaseModel
from datetime import datetime

class APIToken(BaseModel):
    token: str
    user_id: str
    created_at: datetime
