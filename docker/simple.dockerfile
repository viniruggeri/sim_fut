FROM python:3.11-slim

WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Tornar entrypoint executável
RUN chmod +x /app/docker/entrypoint.sh

# Definir entrypoint
ENTRYPOINT ["/app/docker/entrypoint.sh"]
