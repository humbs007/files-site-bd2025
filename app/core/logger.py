import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "buscador_backend.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Formato do log
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] ▶ %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuração do arquivo
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=5)
file_handler.setFormatter(formatter)

# Configuração do console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Logger principal
logger = logging.getLogger("buscador")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
