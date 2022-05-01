FROM python:3.10-slim

WORKDIR /warehouse

COPY ./requirements.txt /warehouse/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /warehouse/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /warehouse/