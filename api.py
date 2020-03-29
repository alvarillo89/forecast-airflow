import hug
import pickle
import pandas as pd
from falcon import HTTP_400, HTTP_200
from datetime import datetime, timedelta


def generate_dates(hour_step):
    """ Genera un rango de horas con un step de 1 hora """
    base = datetime.today().replace(minute=0, second=0, microsecond=0)
    date_list = [base + timedelta(hours=x) for x in range(hour_step)]
    return date_list


# Cargar los modelos de prediccion:
file = open('/tmp/models/arima_temp.pkl', 'rb')
arima_temp = pickle.load(file)
file.close()

file = open('/tmp/models/arima_hum.pkl', 'rb')
arima_hum = pickle.load(file)
file.close()

file = open('/tmp/models/rf_temp.pkl', 'rb')
rf_temp = pickle.load(file)
file.close()

file = open('/tmp/models/rf_hum.pkl', 'rb')
rf_hum = pickle.load(file)
file.close()


# Definir los EndPoints:

# ARIMA:
@hug.get("/servicio/v1/prediccion/{intervalo}")
def version1(intervalo, response):
    if intervalo not in ['24horas', '48horas', '72horas']:
        response.status = HTTP_400
        return "Solo se admiten los siguientes intervalos: 24horas, 48horas y 72horas"
    
    response.status = HTTP_200
    interval = int(intervalo[:2])
    
    # Generar fechas y hacer las predicciones con Arima:
    dates = generate_dates(interval)
    temp = arima_temp.predict(n_periods=interval)
    hum = arima_hum.predict(n_periods=interval)

    # Construir el json de salida:
    return [{"hour": d.strftime("%H:%M"), "temp": t, "hum": h} 
        for d, t, h in zip(dates, temp, hum)]


# RandomForest:
@hug.get("/servicio/v2/prediccion/{intervalo}")
def version1(intervalo, response):
    if intervalo not in ['24horas', '48horas', '72horas']:
        response.status = HTTP_400
        return "Solo se admiten los siguientes intervalos: 24horas, 48horas y 72horas"
    
    response.status = HTTP_200
    interval = int(intervalo[:2])
    
    # Generar fechas:
    dates = generate_dates(interval)
    df = pd.DataFrame({'DATE': dates})
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['DAY'] = df['DATE'].dt.day
    df['HOUR'] = df['DATE'].dt.hour
    df = df.drop(columns='DATE')

    # Predecir:
    temp = rf_temp.predict(df)
    hum = rf_hum.predict(df)

    # Construir el json de salida:
    return [{"hour": d.strftime("%H:%M"), "temp": t, "hum": h} 
        for d, t, h in zip(dates, temp, hum)]