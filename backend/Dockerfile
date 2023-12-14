FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./src /app

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt