import logging
import os
import time
from logging.handlers import RotatingFileHandler
from typing import Optional

from flask import Flask, g, request


def _build_log_path(app: Flask) -> str:
    project_root = os.path.abspath(os.path.join(app.root_path, os.pardir))
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "app.log")


def _ensure_handler(logger: logging.Logger, handler: logging.Handler) -> None:
    for existing in logger.handlers:
        if (
            isinstance(existing, type(handler))
            and getattr(existing, "baseFilename", None)
            == getattr(handler, "baseFilename", None)
        ):
            return
    logger.addHandler(handler)


def setup_logging(app: Flask) -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    file_handler = RotatingFileHandler(
        _build_log_path(app), maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    _ensure_handler(app.logger, file_handler)
    app.logger.propagate = False

    @app.before_request
    def start_timer() -> None:
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        duration_ms = int((time.time() - g.get("start_time", time.time())) * 1000)
        app.logger.info(
            "%s %s %s %sms",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )
        return response

    @app.teardown_request
    def log_exception(error: Optional[BaseException]) -> None:
        if error:
            app.logger.exception("Unhandled exception: %s", error)
