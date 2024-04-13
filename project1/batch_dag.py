# -*- coding: utf-8 -*-
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


dag = DAG('Project_batch_Dataflow_dag',
            catchup=False,
            schedule_interval=None,
            default_args=default_args)


start = DummyOperator(task_id='start',dag=dag)

job = DataflowTemplateOperator(
        task_id='project_template',
        template="gs://magan/template/batchtemplate",
        job_name='project_job_from_airflow',
        location="us-west1",
        dataflow_default_options={
            "project": "ethereal-aria-416604",
            "stagingLocation": "gs://magan/staging",
            "tempLocation": "gs://magan/temp",
            "serviceAccountEmail": "demo-424@ethereal-aria-416604.iam.gserviceaccount.com"},
        parameters={
            "input_path": "gs://magan/data/yelp_academic_dataset_business.json",
            "output_table": "project.business",
            "error_table": "project.error"           
        },
                dag=dag)

start >> job
