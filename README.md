![alt text](https://files.realpython.com/media/Get-Started-With-Django_Watermarked.15a1e05597bc.jpg "Django")
# Despliegue completo de la aplicación web con Docker-Compose 📦

## Requisitos

* Docker-Compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

Verificar la instalación de Docker-Compose:

```
docker-compose -version
```

Si todo ha ido bien, deberá mostrarse una salida similar a la siguiente: `docker-compose version 1.27.4, build 40524192`

## Ejecutar el proyecto

Con una terminal ubicada en la carpeta raíz del proyecto ejecutamos para crear las imágenes y iniciar los contenedores:

```
docker-compose up -d --build
```

Antes de abrir el navegador por primera vez, debemos migrar la base de datos y crear una cuenta de superuser en la aplicación.

```
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py loaddata initialdata.json

docker-compose exec web python manage.py createsuperuser
```

La combinación *email/password* que se introduzca por teclado servirá para acceder al panel de administración de Django ubicado en 127.0.0.1:8000/admin.

## Detener los contenedores

Para detener los contenedores sin borrar el sistema de ficheros se ejecuta el siguiente comando:

```
docker-compose stop
```

Para detener y eliminar los contenedores, redes y volúmenes usados en este proyecto se ejecuta el siguiente comando:

```
docker-compose down
```