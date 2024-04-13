from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG('Stream_Dataflow_dag',
            catchup=False,
            schedule_interval=None,
            default_args=default_args)

output_table= "bal.covid"
output_error_table= "bal.error"

start = DummyOperator(task_id='start',dag=dag)

job = DataflowTemplateOperator(
        task_id='template_stream_job',
        template="gs://magan/template/streamtemplate",
        job_name='job_stream_from_airflow',
        location="us-west1",
        
        dataflow_default_options={
            "project": "ethereal-aria-416604",
            "stagingLocation": "gs://magan/staging",
            "tempLocation": "gs://magan/temp",
            "serviceAccountEmail": "demo-424@ethereal-aria-416604.iam.gserviceaccount.com"},
        parameters={
            "input_subscription": "projects/ethereal-aria-416604/subscriptions/gcp-yelp-stream-sub",
            "output_table": output_table,
            "output_error_table": output_error_table           
        },

                dag=dag)



start >> job
