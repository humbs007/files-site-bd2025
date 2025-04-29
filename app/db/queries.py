from app.db.connection import get_connection

def get_tables_and_indexes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SHOW TABLES")
    tables = [row[f'Tables_in_{conn.database}'] for row in cursor.fetchall()]
    result = {}

    for table in tables:
        cursor.execute(f"SHOW INDEX FROM {table}")
        indexes = cursor.fetchall()
        indexed_fields = list(set(i["Column_name"] for i in indexes if i["Column_name"]))
        result[table] = indexed_fields

    cursor.close()
    conn.close()
    return result
