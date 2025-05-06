import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry
from sqlalchemy import MetaData, Table
from app.core.database import engine

Base = declarative_base()
mapper_registry = registry()

_reflected_tables = {}
_metadata = MetaData()


def get_model_by_table(table_name: str):
    """
    ✅ Retorna um modelo SQLAlchemy refletido dinamicamente da tabela.
    Cache local evita múltiplas reflexões.
    """
    if table_name in _reflected_tables:
        return _reflected_tables[table_name]

    try:
        # Reflete apenas a tabela necessária
        _metadata.reflect(bind=engine, only=[table_name])
        table = Table(
            table_name,
            _metadata,
            autoload_with=engine,
            extend_existing=True
        )

        # Verificação de chave primária
        if not table.primary_key or len(table.primary_key.columns) == 0:
            raise Exception("Tabela sem chave primária detectada.")

        # Criação dinâmica do model
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
        return model_class

    except Exception as e:
        print(f"[table_models] Erro ao refletir tabela '{table_name}': {e}")
        return None
