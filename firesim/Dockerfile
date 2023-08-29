FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./src /src
COPY ./api /api

WORKDIR /api

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
