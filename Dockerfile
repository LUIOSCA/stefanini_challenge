# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Variables para que los logs salgan rápido y no haya basura de caché
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Instalamos dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de tu código
COPY . .

# Puerto estándar de Cloud Run
EXPOSE 8080

# Comando para arrancar la API
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]