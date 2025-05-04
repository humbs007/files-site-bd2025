# backend/app/core/db_schema_config.py

DB_SCHEMA = {
    "banco_meta": {
        "label": "Banco Meta",
        "tables": {
            "table_cemig": {
                "label": "CEMIG",
                "fields": {
                    "id": "ID",
                    "Identificacao": "Identificação",
                    "CPF": "CPF",
                    "Nome": "Nome",
                    "DataNascimento": "Data de Nascimento",
                    "Endereco": "Endereço",
                    "Numero": "Numero",
                    "Complemento": "Complemento",
                    "Bairro": "Bairro",
                    "CEP": "CEP",
                    "Cidade": "Cidade",
                    "UF": "UF",
                    "DDD": "DDD",
                    "Telefone": "Telefone",
                    "consumo_medio": "Consumo Médio",
                    "DDD1": "DDD1",
                    "TELEFONE1": "Telefone 1",
                    "TIPO_TELEFONE": "Tipo Tel",
                    "EMAIL": "e-mail"
                },
                "indices": [
                    {"name": "PRIMARY", "field": "id", "unique": True},
                    {"name": "idx_cpf", "field": "CPF"},
                    {"name": "idx_nome", "field": "Nome"},
                    {"name": "idx_cidade", "field": "Cidade"},
                    {"name": "idx_uf", "field": "UF"},
                    {"name": "idx_telefone", "field": "Telefone"},
                    {"name": "idx_consumo_medio", "field": "consumo_medio"},
                    {"name": "idx_email", "field": "EMAIL"},
                    {"name": "idx_cep", "field": "CEP"},
                    {"name": "idx_tipo_telefone", "field": "TIPO_TELEFONE"}
                ]
            },
            "table_credlink": {
                "label": "CredLink",
                "fields": {
                    "id": "ID",
                    "CPF": "CPF",
                    "NOME": "Nome",
                    "CIDADE": "Cidade",
                    "UF": "UF",
                    "EMAIL": "Email",
                    "FLAG_OBITO": "Flag Óbito",
                    "DT_OBITO": "Data Óbito",
                    "STATUS_RECEITA_FEDERAL": "Status Receita Federal",
                    "PCT_CARGO_SOCIETARIO": "Cargo Societário (%)",
                    "CBO": "CBO",
                    "QT_VEICULOS": "Qtd. Veículos",
                    "RENDA_PRESUMIDA": "Renda Presumida",
                    "FAIXA_RENDA": "Faixa de Renda",
                    "BAIRRO": "Bairro",
                    "TEL_FIXO1": "Telefone Fixo 1",
                    "CELULAR1": "Celular 1"
                },
                "indices": [
                    {"name": "PRIMARY", "field": "id", "unique": True},
                    {"name": "idx_cpf", "field": "CPF"},
                    {"name": "idx_nome", "field": "NOME"},
                    {"name": "idx_bairro", "field": "BAIRRO"},
                    {"name": "idx_cidade", "field": "CIDADE"},
                    {"name": "idx_uf", "field": "UF"},
                    {"name": "idx_flag_obito", "field": "FLAG_OBITO"},
                    {"name": "idx_dt_obito", "field": "DT_OBITO"},
                    {"name": "idx_status_receita_federal", "field": "STATUS_RECEITA_FEDERAL"},
                    {"name": "idx_pct_cargo_societario", "field": "PCT_CARGO_SOCIETARIO"},
                    {"name": "idx_cbo", "field": "CBO"},
                    {"name": "idx_qt_veiculos", "field": "QT_VEICULOS"},
                    {"name": "idx_renda_presumida", "field": "RENDA_PRESUMIDA"},
                    {"name": "idx_faixa_renda", "field": "FAIXA_RENDA"}
                ]
            },
            "table_enel": {
                "label": "ENEL",
                "fields": {
                    "id": "ID",
                    "PN_CPF": "CPF",
                    "PN_CNPJ": "CNPJ",
                    "PN_Nome": "Nome",
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
                    "UF": "UF",
                    "Distrito": "Distrito"
                },
                "indices": [
                    {"name": "idx_energia_cpf", "field": "PN_CPF"},
                    {"name": "idx_energia_cnpj", "field": "PN_CNPJ"},
                    {"name": "idx_energia_regiao", "field": "OL_Regiao"},
                    {"name": "idx_energia_municipio", "field": "OL_Municipio_ObjLig"},
                    {"name": "idx_energia_bairro", "field": "OL_Bairro_ObjLig"},
                    {"name": "idx_energia_distrito", "field": "Distrito"},
                    {"name": "idx_energia_consumo_estimado", "field": "INS_Consumo_Estimado"},
                    {"name": "idx_energia_instalacao", "field": "INS_Instalacao"},
                    {"name": "idx_energia_conta_contrato", "field": "CC_Conta_Contrato"},
                    {"name": "idx_energia_carga_instalada", "field": "INS_Carga_Instalada"}
                ]
            }
            # ... incluir as demais tabelas conforme os dados compartilhados
        },
        "unified_fields": {
            "CPF/CNPJ": ["CPF", "PN_CPF", "CNPJ", "PN_CNPJ", "cpf", "cnpj", "CNPJ_EMPRESA"],
            "UF Geral": ["UF", "PN_UF", "ESTADO", "UF_EMPRESA", "cnpj_uf"],
            "CIDADE Geral": ["CIDADE", "Cidade", "MUNICIPIO_EMPRESA", "OL_Municipio_ObjLig"],
            "Bairro Geral": ["BAIRRO", "Distrito", "OL_Bairro_ObjLig"],
            "CONSUMOS META": [
                "CONSUMO1", "CONSUMO2", "CONSUMO3", "CONSUMO4", "CONSUMO5",
                "CONSUMO6", "CONSUMO7", "CONSUMO8", "CONSUMO9", "CONSUMO10"
            ]
        }
    }
}


def get_all_tables():
    return list(DB_SCHEMA["banco_meta"]["tables"].keys())


def get_table_fields(table: str):
    return list(DB_SCHEMA["banco_meta"]["tables"].get(table, {}).get("fields", {}).keys())


def get_table_indices(table: str):
    return DB_SCHEMA["banco_meta"]["tables"].get(table, {}).get("indices", [])


def get_label(table: str, field: str) -> str:
    return DB_SCHEMA["banco_meta"]["tables"].get(table, {}).get("fields", {}).get(field, field)


def get_table_label(table: str) -> str:
    return DB_SCHEMA["banco_meta"]["tables"].get(table, {}).get("label", table)


def get_unified_fields():
    return DB_SCHEMA["banco_meta"]["unified_fields"]
