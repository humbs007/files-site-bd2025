# backend/app/utils/normalizer.py
CPF_CNPJ_KEYS = {
    "CPF", "PN_CPF", "cpf", "CNPJ", "PN_CNPJ", "cpf_cnpj", "CNPJ_EMPRESA"
}

UNIFIED_GROUPS = {
    "CPF/CNPJ": CPF_CNPJ_KEYS
}

def normalize_field_group(field: str) -> str:
    for group_name, aliases in UNIFIED_GROUPS.items():
        if field in aliases:
            return group_name
    return field

def is_cpf_cnpj_field(field: str) -> bool:
    return field in CPF_CNPJ_KEYS
