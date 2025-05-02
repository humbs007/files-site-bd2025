LABEL_MAP = {
    "PN_CPF": "CPF",
    "PN_CNPJ": "CNPJ",
    "INS_Consumo_Estimado": "Consumo Estimado (kWh)",
    "INS_Carga_Instalada": "Carga Instalada (kW)",
}

def map_labels(row):
    return {LABEL_MAP.get(k, k): v for k, v in row.items()}
