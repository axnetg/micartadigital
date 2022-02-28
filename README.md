![Python 3.10 badge](https://img.shields.io/badge/python-3.10-brightgreen)
![Django 3.2 badge](https://img.shields.io/badge/django-3.2-brightgreen)
[![codecov](https://codecov.io/gh/axnetg/micartadigital/branch/dev/graph/badge.svg?token=lwu6t2UWZe)](https://codecov.io/gh/axnetg/micartadigital)

# Aplicación web de gestión de cartas virtuales para hostelería
Motivado por la tendencia de muchos bares y restaurantes de ofrecer versiones digitales de sus cartas subidas en redes sociales o páginas web, se desarrolla la presente plataforma de gestión y visualización de cartas conforme a las recomendaciones sanitarias derivadas de la pandemia de la COVID-19.

## Objetivos 🎯
Este proyecto tiene como objetivo principal el desarrollo de una plataforma donde los establecimientos de hostelería y restauración puedan crear, modificar y poner a disposición de la clientela sus cartas de forma rápida y sencilla.

## Resumen 📚
Las aplicaciones web consisten en un conjunto de páginas que incluyen elementos con los que el usuario puede interactuar y, en función de ello, generar contenido dinámico para ser visualizado por otros usuarios que visiten el sitio web. Para crearlas es necesario utilizar una base de datos y un lenguaje de programación que trabaje del lado del servidor.

Por ello, normalmente se estructuran en tres capas:
- **Capa de presentación**: facilita el acceso a la aplicación, muestra la información pertinente y proporciona una interfaz gráfica a través de la cual el usuario puede realizar las tareas para las que está diseñada la aplicación.
- **Capa de aplicación**: controla las funcionalidades de la aplicación realizando un procesamiento minucioso de la información que le transmite la capa de presentación y entregando como respuesta los resultados generados.
- **Capa de datos**: gestiona y proporciona mecanismos de persistencia de datos para almacenar y consultar la información necesaria para el correcto funcionamiento de la aplicación.

Para implementar la capa de aplicación existen numerosas herramientas que aceleran y facilitan el desarrollo de una aplicación web denominadas frameworks web. Dichas herramientas se definen como un conjunto de componentes configurables y reutilizables que ofrecen funcionalidades genéricas y comunes a cualquier tipo de sistema web, como bibliotecas para gestión de sesiones, acceso a bases de datos o mecanismos de autenticación y seguridad de datos.

En este proyecto se utiliza el framework web Django, el cual sigue los principios de desarrollo rápido y hace que el programador solo tenga que preocuparse del desarrollo incremental de los requisitos del proyecto. Django es un framework web de alto nivel escrito en Python que permite el desarrollo rápido de sitios web seguros, escalables y mantenibles.

## Arquitectura 📋
Docker es una herramienta diseñada para crear entornos aislados de ejecución de aplicaciones reproducibles mediante el uso de contenedores. Un contenedor ofrece una capa de virtualización de un sistema operativo sobre el cual se empaqueta el código fuente de una aplicación y todas sus dependencias, lo que asegura su ejecución de forma rápida y fiable en cualquier otro entorno informático.

El escenario de uso habitual de Docker en el desarrollo y distribución de aplicaciones consiste en separar cada servicio en contenedores distintos para garantizar la seguridad, asegurar la independencia del hardware virtualizado y proporcionar mecanismos adicionales de gestión de recursos.

Es por esto que los servicios utilizados en el presente sistema software se dividen en contenedores independientes:
- **Contenedor Nginx**: reenvía las peticiones entrantes al servicio de Gunicorn o al directorio de ficheros estáticos, actuando como proxy inverso.
- **Contenedor Gunicorn**: configura el entorno de Python donde se despliega el punto de entrada a la aplicación web siguiendo la especificación WSGI. 
- **Contenedor Postgres**: aloja el sistema gestor de base de datos, donde se almacena la información necesaria para el funcionamiento de la aplicación web.

## Instrucciones de despliegue 🚀
La ejecución de la aplicación requiere desplegar una infraestructura virtual con la ayuda de [Docker](https://docs.docker.com/engine/install/) y [Docker-Compose](https://docs.docker.com/compose/install/). Se describen a continuación los comandos necesarios para su puesta en marcha.

```bash
git clone https://github.com/axnetg/micartadigital
sudo systemctl start docker
sudo docker-compose up -d --build
```

Estos comandos se encargan de descargar una copia local del repositorio, iniciar el daemon de Docker, recuperar las imágenes base de Nginx, Python y Postgres y construir en base a ellas los contenedores. Este proceso puede tardar unos minutos. Tras terminar, el sitio web debe estar accesible en http://localhost:1700.
