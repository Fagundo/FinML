FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y python3.6 \
    sudo \
    wget \
    curl \
    libpq-dev \
    python3-pip

COPY ./FinML /FinML
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /FinML
