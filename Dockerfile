FROM python:3.12.0a1-alpine3.16

USER root

ENV CONF_PATH=/home/config/monitoring.yml
ENV WATCH_FOLDER=/home/config

WORKDIR /home

COPY . /home/

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "src/main.py"]