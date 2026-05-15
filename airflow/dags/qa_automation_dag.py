from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_PATH = "/mnt/d/Sonawane Arnav/College stuff/TY SEM 6/edai"

PYTEST_PATH = "/home/arnav/edai-airflow/airflow_linux_env/bin/pytest"
PYTHON_PATH = "/home/arnav/edai-airflow/airflow_linux_env/bin/python"

default_args = {
    "owner": "arnav",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ai_workflow_qa_automation",
    default_args=default_args,
    description="AI Workflow QA Automation Framework",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["qa", "airflow", "aiworkflow"],
) as dag:

    # Step 1 - Run AI workflow pipeline
    run_pipeline = BashOperator(
        task_id="run_pipeline",
        bash_command=f"""
        cd "{PROJECT_PATH}" &&
        {PYTHON_PATH} -m pipeline.core
        """
    )

    # Step 2 - API Tests
    api_tests = BashOperator(
        task_id="api_tests",
        bash_command=f"""
        cd "{PROJECT_PATH}" &&
        {PYTEST_PATH} tests/api -m api
        """
    )

    # Step 3 - Schema Tests
    schema_tests = BashOperator(
        task_id="schema_tests",
        bash_command=f"""
        cd "{PROJECT_PATH}" &&
        {PYTEST_PATH} -m schema
        """
    )

    # Step 4 - Regression Tests
    regression_tests = BashOperator(
        task_id="regression_tests",
        bash_command=f"""
        cd "{PROJECT_PATH}" &&
        {PYTEST_PATH} tests/regression -m regression
        """
    )

    # Step 5 - Performance Tests
    performance_tests = BashOperator(
        task_id="performance_tests",
        bash_command=f"""
        cd "{PROJECT_PATH}" &&
        {PYTEST_PATH} tests/performance -m performance
        """
    )

    # Step 6 - Generate Reports
    generate_reports = BashOperator(
    	task_id="generate_reports",
    	bash_command=f"""
    	cd "{PROJECT_PATH}" &&

    	TIMESTAMP=$(date +%Y_%m_%d_%H%M%S) &&

    	mkdir -p reports/html_reports &&
    	mkdir -p reports/coverage_reports &&

    	{PYTEST_PATH} tests \
    	--cov=pipeline \
    	--cov-report=html:reports/coverage_reports/coverage_$TIMESTAMP \
    	--html=reports/html_reports/report_$TIMESTAMP.html \
    	--self-contained-html
    	"""
    )

    (
        run_pipeline
        >> api_tests
	>> schema_tests
        >> regression_tests
        >> performance_tests
        >> generate_reports
    )
