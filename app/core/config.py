# backend/app/core/config.py

from sqlalchemy import create_engine

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",               # 👈 ajuste para seu user MySQL real
    "password": "Beto9541!",  # 👈 ajuste para sua senha real
    "database": "banco_meta"        # 👈 Nome REAL do seu banco
}

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
