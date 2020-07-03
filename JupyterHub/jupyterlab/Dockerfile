FROM jupyter/base-notebook

LABEL maintainer="Michael Fagundo <mjfagundo@gmail.com>"

USER root

# Python Packages
COPY requirements.txt .
RUN conda install --yes --file requirements.txt
