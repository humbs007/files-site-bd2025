# backend/Dockerfile
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY ./requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY ./app ./app
COPY ./main.py .
COPY .env .

# Expor porta
EXPOSE 8000

# Comando inicial
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
