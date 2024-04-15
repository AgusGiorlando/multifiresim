FROM python:3.8-slim-buster

COPY ./src /app

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt

WORKDIR /app
EXPOSE 5000
ENV FLASK_APP=/app/index.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
