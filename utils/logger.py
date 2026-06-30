import logging
import sys


def configure_logging(level: str = "INFO", http_client_level: str = "WARNING") -> None:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    else:
        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    logging.getLogger("httpx").setLevel(getattr(logging, http_client_level.upper(), logging.WARNING))
    logging.getLogger("httpcore").setLevel(getattr(logging, http_client_level.upper(), logging.WARNING))


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
