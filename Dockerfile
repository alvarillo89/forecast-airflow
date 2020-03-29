FROM python:3.6-slim

LABEL maintainer="Álvaro alvaro89@correo.ugr.es"
EXPOSE 8080

COPY api.py requirements.txt ./

RUN mkdir /tmp/models/ \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && useradd -m nonroot

USER nonroot

CMD gunicorn -w 4 -b 0.0.0.0:8080 api:__hug_wsgi__