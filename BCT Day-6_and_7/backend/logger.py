import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger

api_logger = setup_logger("blackfalcon.api")
discovery_logger = setup_logger("blackfalcon.discovery")
db_logger = setup_logger("blackfalcon.database")
