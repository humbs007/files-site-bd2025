from decimal import Decimal

def normalize_term(term: str | int | float | Decimal) -> str:
    return ''.join(filter(str.isalnum, str(term))).strip()
