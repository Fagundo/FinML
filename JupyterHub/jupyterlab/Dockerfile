FROM jupyter/base-notebook

LABEL maintainer="Michael Fagundo <mjfagundo@gmail.com>"

USER root

# Python Packages
COPY requirements.txt .
RUN apt-get update \
  && apt-get install -y gcc \
  && python3 -m pip install --upgrade pip \
  && pip install -r requirements.txt
