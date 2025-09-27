import json
import logging
import os
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(env: str = "dev", level: str = "INFO") -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())
    handler = logging.StreamHandler()
    if env == "prod":
        handler.setFormatter(JsonFormatter())
    else:
        formatter = logging.Formatter(
            fmt="%(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
    root.addHandler(handler)


def env_configure_from_vars() -> None:
    configure_logging(env=os.getenv("APP_ENV", "dev"), level=os.getenv("LOG_LEVEL", "INFO"))
