# Forecast Airflow

Microservicio que predice la temperatura y humedad de San Francisco usando Arima y Random Forest Regressor.
Devuelve las predicciones para un intervalo de 24, 48 o 72 horas desde la fecha y hora de la consulta, a 
través de una API RESTful.

Para su despliegue, se emplea un flujo de trabajo diseñado e implementado con Apache Airflow.

Desarrollado para la asignatura Cloud Computing del Máster en Ingerniería Informática (UGR).