FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y python3.6 \
    sudo \
    wget \
    curl \
    libpq-dev \
    python3-pip

COPY ./src /finml
COPY ./requirements.txt ./scripts /home/
RUN pip3 install -r /home/requirements.txt

WORKDIR /finml
