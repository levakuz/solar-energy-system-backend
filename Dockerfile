FROM python:3.11.4-slim
LABEL authors="Kuznetsov Lev, Stepanets Anton"

WORKDIR /opt/
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive
COPY ./ /opt/solar_energy_system
WORKDIR /opt/solar_energy_system
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y curl &&\
    curl -sSL https://install.python-poetry.org | python3.11 - && \
    mkdir /home/root/ && touch /home/root/.bashrc && \
    export PATH="/root/.local/bin:$PATH" && \
    echo export PATH="/root/.local/bin:$PATH" > /home/root/.bashrc && \
    poetry config virtualenvs.create false && poetry install --no-root
