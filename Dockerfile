FROM python:3.6-slim

LABEL maintainer="Álvaro alvaro89@correo.ugr.es"

RUN pip install --upgrade pip

COPY api.py requirements.txt ./
COPY arima_temp.pkl arima_hum.pkl rf_temp.pkl rf_hum.pkl /tmp/

RUN pip install -r requirements.txt

EXPOSE 8080

RUN useradd -m nonroot
USER nonroot

CMD gunicorn -w 4 -b 0.0.0.0:8080 api:__hug_wsgi__