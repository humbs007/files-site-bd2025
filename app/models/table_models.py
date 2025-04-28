from sqlalchemy import Column, Integer, String, BigInteger, Date, DECIMAL, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ================== ENEL - ENERGIA ================== #
class TableEnelEnergia(Base):
    __tablename__ = "table_enel"

    id = Column(Integer, primary_key=True, index=True)
    PN_Parceiro = Column(Integer, nullable=True)
    PN_Nome = Column(String(255), nullable=True)
    PN_BP_Tipo = Column(String(20), nullable=True)
    PN_Genero = Column(String(15), nullable=True)
    PN_CPF = Column(String(11), nullable=True, index=True)
    PN_RG = Column(String(20), nullable=True)
    PN_CNPJ = Column(String(14), nullable=True, index=True)
    PN_Dta_Nasc = Column(Date, nullable=True)
    PN_Idade_PN = Column(Integer, nullable=True)
    PN_Tmp_Criacao_Ano = Column(Integer, nullable=True)
    PN_Fone_Fixo = Column(String(30), nullable=True)
    PN_Fone_Celular = Column(String(30), nullable=True)
    PN_Email = Column(String(255), nullable=True)
    PN_Optin_Email = Column(Integer, nullable=True)
    PN_Optin_SMS = Column(Integer, nullable=True)
    PN_Optin_Bloqueio = Column(Integer, nullable=True)
    CC_Conta_Contrato = Column(BigInteger, nullable=True, index=True)
    CC_Endereco_CC = Column(String(512), nullable=True)
    CC_Parceiro = Column(Integer, nullable=True)
    CC_Banco = Column(String(20), nullable=True)
    CC_Conta_Bancaria = Column(String(50), nullable=True)
    CC_CP_Diapgto = Column(String(15), nullable=True)
    CC_DebAutomatico = Column(Integer, nullable=True)
    CO_Contrato = Column(BigInteger, nullable=True)
    CO_Conta_Contrato = Column(BigInteger, nullable=True)
    CO_Instalacao = Column(BigInteger, nullable=True)
    CO_Tempo_Contrato = Column(Integer, nullable=True)
    CO_Conta_Email = Column(Integer, nullable=True)
    CO_Canal_CEmail = Column(String(20), nullable=True)
    CO_Tempo_CEmail = Column(String(20), nullable=True)
    INS_Instalacao = Column(BigInteger, nullable=True, index=True)
    INS_Loc_Consumo = Column(Integer, nullable=True)
    INS_Carga_Instalada = Column(DECIMAL(15,5), nullable=True, index=True)
    INS_Classe_Subclasse = Column(String(100), nullable=True)
    INS_Status_Instalacao = Column(Integer, nullable=True)
    INS_Nivel_Tensao = Column(Integer, nullable=True)
    INS_Tp_Ligacao = Column(String(20), nullable=True)
    INS_Consumo_Estimado = Column(DECIMAL(15,5), nullable=True, index=True)
    INS_Tp_Instalacao = Column(String(50), nullable=True)
    INS_Un_Leitura = Column(String(20), nullable=True)
    INS_CoodX = Column(String(20), nullable=True)
    INS_CoodY = Column(String(50), nullable=True)
    INS_Obj_Lig = Column(BigInteger, nullable=True)
    INS_Equipamento = Column(String(100), nullable=True)
    INS_Contrato_Concessao = Column(String(100), nullable=True)
    INS_N_Fases = Column(Integer, nullable=True)
    INS_Cod_Indust = Column(String(50), nullable=True)
    INS_Classe = Column(String(30), nullable=True)
    INS_Cat_Tarifa = Column(String(100), nullable=True)
    INS_Classe_Subclasse_C = Column(String(100), nullable=True)
    INS_Status_Instalacao_C = Column(String(50), nullable=True)
    LC_Loc_Consumo = Column(Integer, nullable=True)
    LC_ObjLig = Column(BigInteger, nullable=True)
    OL_ObjLig = Column(BigInteger, nullable=True)
    OL_Municipio_ObjLig = Column(String(100), nullable=True, index=True)
    OL_CEP_GIS = Column(String(10), nullable=True)
    OL_Grupo_CEP = Column(String(30), nullable=True)
    OL_Regiao = Column(String(20), nullable=True, index=True)
    OL_Loc_ObjLig = Column(String(50), nullable=True)
    OL_Bairro_ObjLig = Column(String(100), nullable=True, index=True)
    OL_Conj_ANEEL = Column(String(100), nullable=True)
    OL_End_ObjLig = Column(String(512), nullable=True)
    OL_Circuito_ObjLig = Column(String(100), nullable=True)
    OL_Equip_ObjLig = Column(String(100), nullable=True)
    CPC_Email = Column(String(255), nullable=True)
    CPC_EmailORIGEM = Column(String(50), nullable=True)
    CPC_Celular = Column(String(30), nullable=True)
    CPC_CelularORIGEM = Column(String(50), nullable=True)
    CPC_Fixo = Column(String(30), nullable=True)
    CPC_FixoORIGEM = Column(String(50), nullable=True)
    Distrito = Column(String(100), nullable=True, index=True)
    Forma_Envio = Column(String(50), nullable=True)

# ================== ENEL - META ================== #
class TableEnelMeta(Base):
    __tablename__ = "table_enel"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    PN_Nome = Column(String(255), nullable=True)
    PN_CPF = Column(String(14), nullable=True, index=True)
    PN_CNPJ = Column(String(18), nullable=True, index=True)
    OL_Municipio_ObjLig = Column(String(255), nullable=True)
    OL_Bairro_ObjLig = Column(String(255), nullable=True)
    Distrito = Column(String(255), nullable=True)
    INS_Carga_Instalada = Column(Float, nullable=True)
    INS_Consumo_Estimado = Column(Float, nullable=True)
    CC_Conta_Contrato = Column(Integer, nullable=True)

# ================== META - Endereços ================== #
class TableMeta(Base):
    __tablename__ = "table_meta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    LOGR_TIPO = Column(String(20), nullable=True)
    LOGR_NOME = Column(String(150), nullable=True)
    LOGR_NUMERO = Column(String(20), nullable=True)
    LOGR_COMPLEMENTO = Column(String(50), nullable=True)
    BAIRRO = Column(String(100), nullable=True)
    CIDADE = Column(String(100), nullable=True)
    UF = Column(String(2), nullable=True, index=True)
    CEP = Column(String(8), nullable=True)
    DT_ATUALIZACAO = Column(DateTime, nullable=True)
    DT_INCLUSAO = Column(DateTime, nullable=True)
    TIPO_ENDERECO_ID = Column(String(10), nullable=True)
    CPF = Column(String(11), nullable=True, index=True)
    CONSUMO1 = Column(Text, nullable=True, index=True)
    CONSUMO2 = Column(Text, nullable=True, index=True)
    CONSUMO3 = Column(Text, nullable=True, index=True)
    CONSUMO4 = Column(Text, nullable=True, index=True)
    CONSUMO5 = Column(Text, nullable=True, index=True)
    CONSUMO6 = Column(Text, nullable=True, index=True)
    CONSUMO7 = Column(Text, nullable=True, index=True)
    CONSUMO8 = Column(Text, nullable=True, index=True)
    CONSUMO9 = Column(Text, nullable=True, index=True)
    CONSUMO10 = Column(Text, nullable=True, index=True)

# ================== TELEFONIA - META ================== #
class TableTelefoniaMeta(Base):
    __tablename__ = "table_telefonia"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    cpf_cnpj = Column(String(18), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)

# ================== TELEFONIA ================== #
class TableTelefonia(Base):
    __tablename__ = "table_telefonia"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    cpf_cnpj = Column(String(20), nullable=False)
    nome = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

# ================== HISTÓRICO DE BUSCAS ================== #
class SearchHistory(Base):
    __tablename__ = "searches"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), nullable=True, index=True)
    result = Column(String(255), nullable=True)
