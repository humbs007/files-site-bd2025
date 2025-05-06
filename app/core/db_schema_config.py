# ✅ app/core/db_schema_config.py

# 🎯 Chaves lógicas para filtros unificados
UNIFIED_KEYS = [
    'CPF/CNPJ',
    'UF Geral',
    'CIDADE Geral',
    'Bairro Geral',
    'CONSUMOS META'
]

# 🔗 Campos unificados organizados por tabela
UNIFIED_FIELDS = {
    'table_cemig': {
        'CPF/CNPJ': ['CPF'],
        'UF Geral': ['UF'],
        'CIDADE Geral': ['Cidade'],
        'Bairro Geral': ['Bairro'],
        'CONSUMOS META': []
    },
    'table_credlink': {
        'CPF/CNPJ': ['CPF'],
        'UF Geral': ['UF'],
        'CIDADE Geral': ['CIDADE'],
        'Bairro Geral': ['BAIRRO'],
        'CONSUMOS META': []
    },
    'table_enel': {
        'CPF/CNPJ': ['PN_CPF', 'PN_CNPJ'],
        'UF Geral': ['UF'],
        'CIDADE Geral': ['OL_Municipio_ObjLig'],
        'Bairro Geral': ['OL_Bairro_ObjLig'],
        'CONSUMOS META': ['INS_Consumo_Estimado']
    },
    'table_meta': {
        'CPF/CNPJ': ['CPF'],
        'UF Geral': ['UF'],
        'CIDADE Geral': ['CIDADE'],
        'Bairro Geral': ['BAIRRO'],
        'CONSUMOS META': [
            'CONSUMO1', 'CONSUMO2', 'CONSUMO3', 'CONSUMO4', 'CONSUMO5',
            'CONSUMO6', 'CONSUMO7', 'CONSUMO8', 'CONSUMO9', 'CONSUMO10'
        ]
    },
    'table_plano_saude': {
        'CPF/CNPJ': ['cpf', 'cnpj'],
        'UF Geral': [],
        'CIDADE Geral': [],
        'Bairro Geral': [],
        'CONSUMOS META': []
    },
    'table_vidatoda': {
        'CPF/CNPJ': ['CPF', 'CNPJ_EMPRESA'],
        'UF Geral': ['UF'],
        'CIDADE Geral': ['CIDADE'],
        'Bairro Geral': ['BAIRRO'],
        'CONSUMOS META': []
    }
}

# 🧠 DB_SCHEMA - Apenas para labels amigáveis
DB_SCHEMA = {
    "tabelas": {
        "table_cemig": {
            "nome": "CEMIG",
            "campos": {
                "CPF": "CPF",
                "Nome": "Nome",
                "Cidade": "Cidade",
                "UF": "UF",
                "consumo_medio": "Consumo Médio",
                "EMAIL": "Email",
                "Telefone": "Telefone",
                "TIPO_TELEFONE": "Tipo Telefone",
                "CEP": "CEP",
                "Bairro": "Bairro",
                "DDD": "DDD"
            }
        },
        "table_credlink": {
            "nome": "CredLink",
            "campos": {
                "CPF": "CPF",
                "NOME": "Nome",
                "CIDADE": "Cidade",
                "UF": "UF",
                "BAIRRO": "Bairro",
                "EMAIL": "Email",
                "CELULAR1": "Celular 1",
                "QT_VEICULOS": "Qtd. Veículos",
                "RENDA_PRESUMIDA": "Renda Presumida",
                "FLAG_OBITO": "Flag Óbito"
            }
        },
        "table_enel": {
            "nome": "ENEL",
            "campos": {
                "PN_CPF": "CPF",
                "PN_CNPJ": "CNPJ",
                "PN_NOME": "Nome",
                "PN_Email": "Email",
                "PN_Fone_Celular": "Celular",
                "PN_Fone_Fixo": "Telefone Fixo",
                "OL_Bairro_ObjLig": "Bairro",
                "OL_Municipio_ObjLig": "Município",
                "OL_Regiao": "Região",
                "INS_Consumo_Estimado": "Consumo Estimado",
                "INS_Carga_Instalada": "Carga Instalada",
                "INS_Instalacao": "Instalação",
                "CC_Conta_Contrato": "Conta Contrato",
                "UF": "UF"
            }
        },
        "table_meta": {
            "nome": "META",
            "campos": {
                "CPF": "CPF",
                "UF": "UF",
                "BAIRRO": "Bairro",
                "CIDADE": "Cidade",
                "DT_ATUALIZACAO": "Data Atualização",
                "CONSUMO1": "Consumo 1",
                "CONSUMO2": "Consumo 2",
                "CONSUMO3": "Consumo 3",
                "CONSUMO4": "Consumo 4",
                "CONSUMO5": "Consumo 5",
                "CONSUMO6": "Consumo 6",
                "CONSUMO7": "Consumo 7",
                "CONSUMO8": "Consumo 8",
                "CONSUMO9": "Consumo 9",
                "CONSUMO10": "Consumo 10"
            }
        },
        "table_plano_saude": {
            "nome": "PLANO SAÚDE",
            "campos": {
                "cnpj": "CNPJ",
                "operadora": "Operadora",
                "nome": "Nome",
                "cpf": "CPF",
                "email": "Email",
                "valor": "Valor",
                "telefone1": "Telefone 1",
                "telefone_empresa": "Telefone da Empresa",
                "qtd_vidas": "Qtd. Vidas"
            }
        },
        "table_vidatoda": {
            "nome": "VIDATODA",
            "campos": {
                "CPF": "CPF",
                "NOME": "Nome",
                "MAE": "Nome da Mãe",
                "NASCIMENTO": "Nascimento",
                "ENDERECO": "Endereço",
                "BAIRRO": "Bairro",
                "CIDADE": "Cidade",
                "UF": "UF",
                "CEP": "CEP",
                "TELEFONE": "Telefone",
                "PIS": "PIS",
                "CBO": "CBO",
                "OCUPACAO": "Ocupação",
                "CNPJ_EMPRESA": "CNPJ Empresa",
                "RAZAO_EMPRESA": "Razão Empresa",
                "SALARIO_EMPRESA": "Salário Empresa"
            }
        }
    }
}
