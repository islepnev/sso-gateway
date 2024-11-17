from sqlalchemy import create_engine, MetaData
from databases import Database
from itsdangerous import URLSafeTimedSerializer
from keycloak import KeycloakOpenID
from app.utils.config_manager import ConfigManager
from app.utils.config import AppConfig
from app.models.tables import metadata

class AppContext:
    def __init__(self):
        self._config: AppConfig = None
        self._database: Database = None
        self._engine = None
        self._serializer = None
        self._keycloak_openid = None

    def load_config(self, config_path: str = "config/config.yaml", secrets_path: str = "config/secrets.yaml"):
        """
        Load configuration and prepare AppConfig instance.
        """
        ConfigManager.load_config(config_path, secrets_path)
        self._config = ConfigManager.get_config()

    @property
    def config(self) -> AppConfig:
        if self._config is None:
            raise ValueError("Configuration is not loaded.")
        return self._config

    @property
    def database(self) -> Database:
        if self._database is None:
            database_url = self.config.gateway.database_url
            self._database = Database(database_url)
        return self._database

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self.config.gateway.database_url,
                connect_args={"check_same_thread": False}
            )
            # Use the metadata defined in models/tables.py to create all tables
            metadata.create_all(self._engine)
        return self._engine

    @property
    def serializer(self) -> URLSafeTimedSerializer:
        if self._serializer is None:
            self._serializer = URLSafeTimedSerializer(self.config.keycloak.client_secret)
        return self._serializer

    @property
    def keycloak_openid(self) -> KeycloakOpenID:
        if self._keycloak_openid is None:
            keycloak_config = self.config.keycloak
            self._keycloak_openid = KeycloakOpenID(
                server_url=keycloak_config.server_url,
                realm_name=keycloak_config.realm,
                client_id=keycloak_config.client_id,
                client_secret_key=keycloak_config.client_secret,
                verify=keycloak_config.verify_ssl,
            )
        return self._keycloak_openid

    async def startup(self):
        """
        Start services (e.g., connect to the database).
        """
        await self.database.connect()

    async def shutdown(self):
        """
        Shutdown services (e.g., disconnect from the database).
        """
        await self.database.disconnect()
