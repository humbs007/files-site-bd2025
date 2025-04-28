import re
from fastapi import HTTPException

def validate_cpf(cpf: str) -> str:
    if not re.fullmatch(r'\d{11}', cpf):
        raise HTTPException(status_code=400, detail="CPF inválido. Deve conter 11 dígitos numéricos.")
    return cpf

def validate_cnpj(cnpj: str) -> str:
    if not re.fullmatch(r'\d{14}', cnpj):
        raise HTTPException(status_code=400, detail="CNPJ inválido. Deve conter 14 dígitos numéricos.")
    return cnpj
