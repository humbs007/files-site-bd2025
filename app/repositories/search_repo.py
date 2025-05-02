from sqlalchemy.sql import text

def run_custom_query(connection, query_str: str, params: dict):
    return connection.execute(text(query_str), params).mappings().all()
