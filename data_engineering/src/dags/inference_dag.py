from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'inference_dag',
    default_args=default_args,
    description='DAG para ejecutar inferencia con un modelo en Docker',
    schedule_interval='0 0 * * *',
)

run_inference_task = DockerOperator(
    task_id='run_inference',
    image='inference-executor:latest',
    api_version='auto',
    auto_remove=True,
    dag=dag,
)

# Definir el orden de ejecución
run_inference_task