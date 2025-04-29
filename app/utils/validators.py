import re

def validate_cpf(cpf: str) -> bool:
    return bool(re.match(r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$", cpf))

def validate_cnpj(cnpj: str) -> bool:
    return bool(re.match(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$", cnpj))

def validate_cep(cep: str) -> bool:
    return bool(re.match(r"^\d{5}-\d{3}$", cep))

def format_data(data: str) -> str:
    # Se precisar tratar datas em DD/MM/AAAA
    return data.replace("/", "-")
