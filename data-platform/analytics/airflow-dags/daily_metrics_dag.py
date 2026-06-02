"""Orchestrates the nightly dbt run + downstream reporting export."""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("daily_metrics", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False) as dag:
    dbt_run = BashOperator(task_id="dbt_run", bash_command="dbt run --project-dir data-platform/analytics/dbt_project")
