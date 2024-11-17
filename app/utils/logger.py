import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

def configure_logging(level: str, format: str):
    logging.getLogger().setLevel(level.upper())
    for handler in logging.getLogger().handlers:
        handler.setFormatter(logging.Formatter(format))
