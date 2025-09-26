FROM python:3.11-slim

WORKDIR /app

# Copiar e instalar dependências básicas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit precisa do `watchdog`
RUN pip install --no-cache-dir streamlit watchdog

# Copiar código fonte
COPY . .

# Tornar entrypoint executável
RUN chmod +x /app/docker/entrypoint.sh

# Expor porta do Streamlit
EXPOSE 8501

# Definir entrypoint
ENTRYPOINT ["/app/docker/entrypoint.sh"]
