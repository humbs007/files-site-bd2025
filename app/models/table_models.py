# ✅ app/models/table_models.py

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table
from app.core.database import engine

Base = declarative_base()
_reflected_tables = {}

def get_model_by_table(table_name: str):
    if table_name in _reflected_tables:
        return _reflected_tables[table_name]

    try:
        local_metadata = MetaData()
        local_metadata.reflect(bind=engine, only=[table_name])

        table = Table(
            table_name,
            local_metadata,
            autoload_with=engine,
            extend_existing=True
        )

        if not table.primary_key or len(table.primary_key.columns) == 0:
            raise Exception(f"Tabela '{table_name}' não possui chave primária.")

        model_class = type(
            f"{table_name.capitalize()}Model",
            (Base,),
            {
                '__table__': table,
                '__tablename__': table_name,
                '__repr__': lambda self: f"<{table_name} {getattr(self, 'id', '')}>"
            }
        )

        _reflected_tables[table_name] = model_class
        print(f"[DEBUG] Model carregado para {table_name}")
        return model_class

    except Exception as e:
        print(f"[ERRO] Falha ao refletir tabela '{table_name}': {e}")
        return None
