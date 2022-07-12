FROM python:3.8-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean
    
COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/