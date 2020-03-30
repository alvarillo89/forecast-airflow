import os
import pickle
import pandas as pd
import pmdarima as pm
from zipfile import ZipFile
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor


def populate_db(df):
    """ Almacena en MongoDB los datos contenidos en un DataFrame """
    client = MongoClient('localhost', 27017)
    db = client['forecast']['temp_hum']
    db.insert_one({'index': 'forecast', 'data': df.to_dict('records')})
    client.close()


def clean_and_store_data():
    """ Descomprime, une y limpia ambos csvs. A continuación, almacena
    los datos en MongoDB llamando a la función populate_db 
    """
    with ZipFile('/tmp/humidity.csv.zip', 'r') as file:
        file.extractall('/tmp/')
    
    with ZipFile('/tmp/temperature.csv.zip', 'r') as file:
        file.extractall('/tmp/')

    hum = pd.read_csv("/tmp/humidity.csv")[['datetime', 'San Francisco']]
    temp = pd.read_csv("/tmp/temperature.csv")[['datetime', 'San Francisco']]
    # Renombrar las columnas:
    hum = hum.rename(columns = {'datetime': 'DATE', 'San Francisco': 'HUM'})
    temp = temp.rename(columns = {'datetime': 'DATE', 'San Francisco': 'TEMP'})
    # Merge:
    df = pd.merge(temp, hum, on='DATE')
    # Borrar los NaN:
    df = df.dropna()
    # Guardar:
    populate_db(df)


def get_data_from_db():
    """ Obtiene los datos de temperatura y humedad desde MongoDB.
    Devuelve un DataFrame de Pandas 
    """
    client = MongoClient('localhost', 27017)
    db = client['forecast']['temp_hum']
    data_from_db = db.find_one({'index': 'forecast'})
    df = pd.DataFrame(data_from_db['data'])
    client.close()
    return df


def train_arima():
    """ Entrena dos modelos para realizar las predicciones usando ARIMA.
    Uno para temperatura y otro para humedad.
    Guarda los modelos entrenados en un fichero .pkl
    """
    df = get_data_from_db()

    # Puesto que arima tarda demasiado en ejecutarse, entrenamos
    # con un subconjunto de los datos:
    df = df.sample(10000, random_state=89)

    # Crear el directorio objetivo si no existe:
    if not os.path.exists('/tmp/models/'):
        os.mkdir('/tmp/models/')

    with open('/tmp/models/arima_temp.pkl', 'wb') as pkl:
        model = pm.auto_arima(df.TEMP, start_p=1, start_q=1,
            test='adf', max_p=3, max_q=3, m=1, d=None,           
            seasonal=False, start_P=0, D=0, trace=True, 
            error_action='ignore', suppress_warnings=True, 
            stepwise=True)

        pickle.dump(model, pkl)

    with open('/tmp/models/arima_hum.pkl', 'wb') as pkl:
        model = pm.auto_arima(df.HUM, start_p=1, start_q=1,
            test='adf', max_p=3, max_q=3, m=1, d=None,           
            seasonal=False, start_P=0, D=0, trace=True, 
            error_action='ignore', suppress_warnings=True, 
            stepwise=True)

        pickle.dump(model, pkl)

    
def train_random_forest():
    """ Entrena dos modelos para realizar las predicciones usando un
    Random Forest Regressor de sklearn.
    Guarda los modelos entrenados en un fichero .pkl
    """
    df = get_data_from_db()

    # Crear el directorio objetivo si no existe:
    if not os.path.exists('/tmp/models/'):
        os.mkdir('/tmp/models/')

    # Preprocesar:
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d %H:%M:%S")
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['DAY'] = df['DATE'].dt.day
    df['HOUR'] = df['DATE'].dt.hour
    df = df.drop(columns='DATE')

    # Crear conjuntos de train y etiquetas:
    X = df[["YEAR", "MONTH", "DAY", "HOUR"]]
    y_temp = df["TEMP"]
    y_hum = df["HUM"]

    with open('/tmp/models/rf_temp.pkl', 'wb') as pkl:
        regr = RandomForestRegressor(n_jobs=-1).fit(X, y_temp)
        pickle.dump(regr, pkl)

    with open('/tmp/models/rf_hum.pkl', 'wb') as pkl:
        regr = RandomForestRegressor(n_jobs=-1).fit(X, y_hum)
        pickle.dump(regr, pkl)