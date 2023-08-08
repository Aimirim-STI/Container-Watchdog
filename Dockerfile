FROM python:3.11-alpine3.18

USER root

ENV CONF_PATH=/home/config/monitoring.yml
ENV WATCH_FOLDER=/home/config

WORKDIR /home

COPY . /home/

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "src/main.py"]