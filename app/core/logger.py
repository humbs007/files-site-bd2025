# ✅ backend/app/core/logger.py

import logging
import sys
import os

# 🔧 Nível de log configurável por variável de ambiente
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("buscador")
logger.setLevel(LOG_LEVEL)

# 🧹 Evita duplicação em reloads do uvicorn
if logger.hasHandlers():
    logger.handlers.clear()

# 📤 Saída no console padrão
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(LOG_LEVEL)

# 📋 Formato padronizado (sem emoji para compatibilidade)
formatter = logging.Formatter(
    fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
