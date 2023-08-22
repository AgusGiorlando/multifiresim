# Usa una imagen de Linux como base
# FROM ubuntu:latest
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


# Instala las dependencias necesarias para compilar y ejecutar la aplicación
# RUN apt-get update && apt-get install -y gcc

# Copia los archivos de la aplicación a la imagen
COPY ./api /api
COPY ./src /src

# Establece el directorio de trabajo dentro de la imagen
WORKDIR /api/

#Install the package dependencies in the requirements file.
# RUN pip install fastapi uvicorn

# Compila la aplicación
#RUN gcc -o fireSim fireSim.c
##RUN make /app

# Comando predeterminado para ejecutar la aplicación en el contenedor
# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
