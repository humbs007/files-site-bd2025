# backend/app/core/logger.py

import logging
import sys
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("buscador")
logger.setLevel(LOG_LEVEL)

# Limpa handlers anteriores (evita duplicações em reload)
if logger.hasHandlers():
    logger.handlers.clear()

# StreamHandler para stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(LOG_LEVEL)

# Formatter seguro (sem emojis para terminais Windows)
formatter = logging.Formatter(
    fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
