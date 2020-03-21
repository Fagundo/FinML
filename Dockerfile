FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y python3.6 \
    sudo \
    wget \
    curl \
    python3-pip

COPY ./finml /finml
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
