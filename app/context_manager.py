from app.context import AppContext

app_context = AppContext()

def initialize_context(config_path="config/config.yaml", secrets_path="config/secrets.yaml"):
    app_context.load_config()
    app_context.database
    return app_context