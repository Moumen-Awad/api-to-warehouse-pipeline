from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="api_to_warehouse_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["simple-project"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python $AIRFLOW_HOME/include/src/extract.py"
    )

    load = BashOperator(
        task_id="load",
        bash_command="python $AIRFLOW_HOME/include/src/load.py"
    )

    transform = BashOperator( 
        task_id="transform", 
        bash_command="cd $AIRFLOW_HOME/include/warehouse_dbt && dbt run --profiles-dir .",
    )

    extract >> load >> transform