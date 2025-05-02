# backend/app/utils/validators.py

from typing import List

ALLOWED_OPERATORS = ['=', '!=', '>', '<', '>=', '<=']

def is_valid_operator(op: str) -> bool:
    return op in ALLOWED_OPERATORS

def sanitize_identifier(name: str) -> bool:
    """
    Impede SQL injection: apenas letras, números e underline.
    """
    return name.replace("_", "").isalnum()

def remove_duplicates(fields: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in fields:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
