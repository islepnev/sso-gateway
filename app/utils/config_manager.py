from typing import Optional
from app.utils.config import AppConfig, KeycloakConfig, GatewayConfig, LoggingConfig
import yaml
from pathlib import Path
import logging

from app.utils.logger import configure_logging

logger = logging.getLogger(__name__)


class ConfigManager:
    _config: Optional[AppConfig] = None

    @classmethod
    def load_config(cls, config_path: str = "config/config.yaml", secrets_path: str = "config/secrets.yaml") -> None:
        """Load configuration and merge secrets."""
        try:
            # Load main config
            with Path(config_path).open() as f:
                main_config = yaml.safe_load(f) or {}

            # Load secrets
            secrets_config = {}
            secrets_file = Path(secrets_path)
            if secrets_file.exists():
                with secrets_file.open() as f:
                    secrets_config = yaml.safe_load(f) or {}

            # Merge configs (secrets override main config)
            merged_config = {**main_config, **secrets_config}

            # Parse into AppConfig
            cls._config = AppConfig(
                keycloak=KeycloakConfig(**merged_config["keycloak"]),
                gateway=GatewayConfig(**merged_config["gateway"]),
                logging=LoggingConfig(**merged_config.get("logging", {})),
            )

            # Update logging after config is loaded
            configure_logging(cls._config.logging.level, cls._config.logging.format)

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise ValueError(f"Configuration could not be loaded: {e}")

    @classmethod
    def get_config(cls) -> AppConfig:
        """Provide access to the configuration."""
        if cls._config is None:
            raise ValueError("Configuration has not been loaded. Call `load_config` first.")
        return cls._config
