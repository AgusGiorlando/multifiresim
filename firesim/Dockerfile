FROM python:3.9

COPY ./src /src
COPY ./api /api

COPY requirements.txt /
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
# RUN mkdir -p /api/results

WORKDIR /api/src

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]
