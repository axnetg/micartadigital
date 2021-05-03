![Django](https://files.realpython.com/media/Get-Started-With-Django_Watermarked.15a1e05597bc.jpg)
![Python 3.9 badge](https://img.shields.io/badge/python-3.9-brightgreen)
![Django 3.2 badge](https://img.shields.io/badge/django-3.2-brightgreen)

# Despliegue completo de la aplicación 📦

## Requisitos

Instalar Docker-Compose.

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

Verificar la instalación de Docker-Compose:

```
docker-compose --version
```

Si todo ha ido bien, deberá mostrarse una salida similar a la siguiente: `docker-compose version 1.29.0, build 07737305`

## Ejecutar el proyecto

Con una terminal ubicada en la carpeta raíz del proyecto ejecutamos para crear las imágenes e iniciar los contenedores:

```
docker-compose up -d --build
```

Una vez se hayan levantado todos los contenedores, abrir un navegador y acceder a localhost:1700 para entrar a la página de inicio del proyecto.

Si se desea rellenar la base de datos con usuarios, establecimientos y cartas de ejemplo debe ejecutarse a mayores el siguiente comando:

```
docker-compose exec web python manage.py loaddata ../initialdata.json
```

Para obtener una cuenta de superusuario con permisos para acceder al panel de administración de Django, debe crearse a través de la terminal con el siguiente comando:

```
docker-compose exec web python manage.py createsuperuser
```

## Detener los contenedores

Para detener los contenedores sin eliminarlos se ejecuta el siguiente comando:

```
docker-compose stop
```

Para detener y eliminar los contenedores, redes y volúmenes usados en este proyecto se ejecuta el siguiente comando:

```
docker-compose down
```