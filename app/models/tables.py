from sqlalchemy import Table, Column, String, DateTime, Boolean, MetaData, func
from datetime import datetime

metadata = MetaData()

api_tokens = Table(
    "api_tokens",
    metadata,
    Column("token", String, primary_key=True, index=True),
    Column("user_id", String, nullable=False, index=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    # Column("created_at", DateTime, default=datetime.utcnow),
    Column("expires_at", DateTime, nullable=True),
    Column("revoked", Boolean, default=False),
)
