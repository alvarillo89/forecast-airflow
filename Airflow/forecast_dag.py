# Airflow modules:
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Complements:
from forecast.pycomplements import *

##############################################
## SETUP:
##############################################

# DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Init DAG
dag = DAG(
    'Forecast',
    default_args=default_args,
    description='Assignment 2 dag',
    schedule_interval='@once',
    catchup=False
)

##############################################
## TASKS:
##############################################

StartDB = BashOperator(
    task_id="StartDB",
    depends_on_past=False,
    bash_command="docker run -d --rm -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4",
    dag=dag
)

GetDataHumidity = BashOperator(
    task_id="GetDataHumidity",
    depends_on_past=False,
    bash_command="curl -o /tmp/humidity.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/humidity.csv.zip",
    dag=dag
)

GetDataTemperature = BashOperator(
    task_id="GetDataTemperature",
    depends_on_past=False,
    bash_command="curl -o /tmp/temperature.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/temperature.csv.zip",
    dag=dag
)

CleanStore = PythonOperator(
    task_id="CleanStore",
    depends_on_past=False,
    python_callable=clean_and_store_data,
    dag=dag
)

TrainArima = PythonOperator(
    task_id="TrainArima",
    depends_on_past=False,
    python_callable=train_arima,
    dag=dag
)

TrainRF = PythonOperator(
    task_id="TrainRF",
    depends_on_past=False,
    python_callable=train_random_forest,
    dag=dag
)

CloneRepo = BashOperator(
    task_id="CloneRepo",
    depends_on_past=False,
    bash_command="git clone https://github.com/alvarillo89/forecast-airflow.git /tmp/forecast-airflow/",
    dag=dag
)

UnitTest = BashOperator(
    task_id="UnitTest",
    depends_on_past=False,
    bash_command="cd /tmp/forecast-airflow/ && python3 tests.py",
    dag=dag
)

Build = BashOperator(
    task_id="Build",
    depends_on_past=False,
    bash_command="cd /tmp/forecast-airflow/ && docker build --rm -t api:latest .",
    dag=dag
)

Deploy = BashOperator(
    task_id="Deploy",
    depends_on_past=False,
    bash_command="docker run -d --rm --name api -v /tmp/models/:/tmp/models/ -p 8080:8080 api:latest",
    dag=dag
)

##############################################
## DAG CONNECTIONS:
##############################################

StartDB >> [GetDataHumidity, GetDataTemperature] >> CleanStore >> [TrainArima, TrainRF] >> CloneRepo >> UnitTest >> Build >> Deploy