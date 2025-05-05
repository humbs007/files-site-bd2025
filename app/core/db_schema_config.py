DB_SCHEMA = {
    "tabelas": {
        "table_cemig": {
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
            "campos": {
                "PN_CPF": "CPF",
                "PN_CNPJ": "CNPJ",
                "PN_NOME": "Nome",
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
            "campos": {
                "cnpj": "CNPJ",
                "operadora": "Operadora",
                "nome": "Nome",
                "cpf": "CPF",
                "valor": "Valor",
                "telefone_empresa": "Telefone da Empresa",
                "qtd_vidas": "Qtd. Vidas"
            }
        },
        "table_vidatoda": {
            "campos": {
                "CPF": "CPF",
                "NOME": "Nome",
                "MAE": "Nome da Mãe",
                "NASCIMENTO": "Nascimento",
                "BAIRRO": "Bairro",
                "CIDADE": "Cidade",
                "UF": "UF",
                "CEP": "CEP",
                "PIS": "PIS",
                "CBO": "CBO",
                "OCUPACAO": "Ocupação",
                "CNPJ_EMPRESA": "CNPJ Empresa",
                "RAZAO_EMPRESA": "Razão Empresa",
                "SALARIO_EMPRESA": "Salário Empresa"
            }
        }
    },

    "unificados": {
        "CPF/CNPJ": [
            "CPF", "PN_CPF", "CNPJ", "PN_CNPJ", "cpf", "cnpj", "CNPJ_EMPRESA"
        ],
        "UF Geral": [
            "UF", "UF_EMPRESA"
        ],
        "CIDADE Geral": [
            "Cidade", "CIDADE", "OL_Municipio_ObjLig", "MUNICIPIO_EMPRESA"
        ],
        "Bairro Geral": [
            "BAIRRO", "Bairro", "OL_Bairro_ObjLig", "Distrito"
        ],
        "CONSUMOS META": [
            "CONSUMO1", "CONSUMO2", "CONSUMO3", "CONSUMO4", "CONSUMO5",
            "CONSUMO6", "CONSUMO7", "CONSUMO8", "CONSUMO9", "CONSUMO10"
        ]
    }
}
