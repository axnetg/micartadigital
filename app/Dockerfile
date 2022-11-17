# Imagen base
FROM python:3.11-slim

# Autor
LABEL maintainer="avrodriguez17@esei.uvigo.es"

# Establecer directorio de trabajo
WORKDIR /app/www

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Abrir puerto de entrada
EXPOSE 8000

# Copiar proyecto
COPY . /app
RUN chmod 755 ../wait-for-it.sh
