FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ./requirements.txt .
RUN apt-get update && apt-get upgrade -y && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
