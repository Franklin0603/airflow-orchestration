"""
A simple DAG to run dbt models daily.
"""
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from pendulum import datetime
import os

# Get Airflow variables
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "/usr/local/airflow/dbt")
PROFILES_DIR = os.getenv("PROFILES_DIR", "/usr/local/airflow/include/dbt/profiles")
DBT_TARGET = os.getenv("DBT_TARGET", "dev")

@dag(
    schedule_interval="0 5 * * *",  # 5 AM UTC daily
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["dbt"],
    default_args={
        "owner": "astro",
        "retries": 1,
    },
)
def dbt_daily():
    """
    A simple DAG that runs dbt models on a daily schedule.
    """
    
    # Define path to dbt execution script
    dbt_script_path = "/Users/franklinajisogun/Documents/engineering-development/dbt/tpch-project/airflow-project/include/dbt/scripts/run_dbt.sh"
    
    # Task to run dbt source freshness
    dbt_source_freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command=f"{dbt_script_path} 'source freshness' {DBT_TARGET}",
    )
    
    # Group for staging models
    with TaskGroup(group_id="staging") as staging_group:
        run_staging = BashOperator(
            task_id="run_staging",
            bash_command=f"{dbt_script_path} run {DBT_TARGET} staging",
        )
        
        test_staging = BashOperator(
            task_id="test_staging",
            bash_command=f"{dbt_script_path} test {DBT_TARGET} staging",
        )
        
        run_staging >> test_staging
    
    # Group for marts models
    with TaskGroup(group_id="marts") as marts_group:
        run_marts = BashOperator(
            task_id="run_marts",
            bash_command=f"{dbt_script_path} run {DBT_TARGET} marts",
        )
        
        test_marts = BashOperator(
            task_id="test_marts",
            bash_command=f"{dbt_script_path} test {DBT_TARGET} marts",
        )
        
        run_marts >> test_marts
    
    # Generate dbt documentation
    dbt_docs_generate = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=f"{dbt_script_path} docs generate {DBT_TARGET}",
    )
    
    # Define task dependencies
    dbt_source_freshness >> staging_group >> marts_group >> dbt_docs_generate

# Initialize the DAG
dbt_daily_dag = dbt_daily()