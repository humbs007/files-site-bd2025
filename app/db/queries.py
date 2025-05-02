from app.db.connection import engine
from sqlalchemy import text

def get_tables_and_indexes():
    result = {}

    with engine.connect() as connection:
        # Buscar todas tabelas
        tables_query = text("SHOW TABLES")
        tables_result = connection.execute(tables_query).fetchall()

        tables = [row[0] for row in tables_result]  # 👈 Corrigido: pegar a primeira coluna diretamente

        for table in tables:
            # Buscar índices de cada tabela
            index_query = text(f"SHOW INDEX FROM {table}")
            index_result = connection.execute(index_query).fetchall()

            indexed_fields = []
            for row in index_result:
                try:
                    col_name = row["Column_name"]  # 👈 SHOW INDEX sempre tem coluna "Column_name"
                    if col_name and col_name not in indexed_fields:
                        indexed_fields.append(col_name)
                except (KeyError, TypeError):
                    # fallback para pegar posição se necessário
                    if len(row) >= 5:
                        col_name = row[4]
                        if col_name and col_name not in indexed_fields:
                            indexed_fields.append(col_name)

            result[table] = indexed_fields

    return result
