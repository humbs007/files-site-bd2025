ALLOWED_OPERATORS = ['=', '!=', '>=', '<=', '>', '<']

def validate_table_and_field(name: str) -> str:
    if not name.replace("_", "").isalnum():
        raise ValueError(f"Nome inválido: {name}")
    return name

def validate_operator(op: str) -> str:
    if op not in ALLOWED_OPERATORS:
        raise ValueError(f"Operador não permitido: {op}")
    return op
