from app.db.connection import get_connection

def validate_operator(op):
    return op in ["=", ">", "<", ">=", "<="]

def get_indexed_fields(table):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SHOW INDEX FROM {table}")
    indexes = cursor.fetchall()
    fields = list(set(i["Column_name"] for i in indexes if i["Column_name"]))
    cursor.close()
    conn.close()
    return fields

def get_column_type(table, column):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SHOW FIELDS FROM {table} WHERE Field = %s", (column,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return result["Type"]  # Ex: decimal(15,5), varchar(255), int
    return "varchar"
