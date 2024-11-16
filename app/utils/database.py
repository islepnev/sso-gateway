from sqlalchemy import MetaData, Table, Column, String, DateTime
from sqlalchemy.sql import func
from app.context_manager import app_context

metadata = MetaData()

api_tokens = Table(
    "api_tokens",
    metadata,
    Column("token", String, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

def get_database():
    return app_context.database

def get_engine():
    return app_context.engine


# # Lazy initialized objects
# _database = None
# _engine = None


# def get_database() -> Database:
#     """
#     Lazily initialize and return the Database instance.
#     """
#     global _database
#     if _database is None:
#         config = ConfigManager.get_config()
#         database_url = config.gateway.database_url
#         _database = Database(database_url)
#     return _database


# def get_engine() -> create_engine:
#     """
#     Lazily initialize and return the SQLAlchemy Engine instance.
#     """
#     global _engine
#     if _engine is None:
#         config = ConfigManager.get_config()
#         database_url = config.gateway.path  # Replace with appropriate config value if database URL is in config
#         _engine = create_engine(database_url, connect_args={"check_same_thread": False})
#         metadata.create_all(_engine)  # Ensure tables are created
#     return _engine
