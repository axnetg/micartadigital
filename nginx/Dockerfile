# Imagen base
FROM nginx:1.21-alpine

# Autor
LABEL maintainer="avrodriguez17@esei.uvigo.es"

# Copiar fichero de configuración
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
