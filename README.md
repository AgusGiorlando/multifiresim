# Multifiresim

## Descripción
Multifiresim es una plataforma diseñada para la ejecución de simuladores de comportamiento de incendios forestales en la nube. La plataforma integra una interfaz de usuario web, una API backend, una base de datos MongoDB y una adaptación del simulador de incendios forestales Firesim, cada componente ejecutándose en su propio contenedor Docker.

## Componentes
La plataforma Multifiresim está compuesta por cuatro servicios principales:
1. **Frontend**: Una interfaz web construida con Python y Flask.
2. **Backend**: Una API diseñada con Python y el framework FastAPI.
3. **Base de datos**: MongoDB para la gestión de datos.
4. **Firesim**: Una adaptación del simulador de incendios forestales, también usando FastAPI.

## Requisitos Previos
Para ejecutar Multifiresim, asegúrate de tener instalado [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) en tu sistema. Estas herramientas son necesarias para construir y ejecutar los contenedores definidos en el archivo de configuración de Docker.

## Despliegue
Para desplegar la plataforma Multifiresim, sigue estos pasos:

1. Clona el repositorio de Multifiresim:
   ```bash
   git clone https://github.com/AgusGiorlando/multifiresim.git
   cd multifiresim/mft
   ```
2. Ejecuta Docker Compose:
    ```bash
    docker-compose up -d
    ```
## Uso
Una vez que los servicios estén en ejecución, podrás acceder a la interfaz de usuario de Multifiresim a través de tu navegador ingresando a http://localhost:8000 (reemplaza puerto con el puerto configurado para el servicio frontend en tu docker-compose.yaml).