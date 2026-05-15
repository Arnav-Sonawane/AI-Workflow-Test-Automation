# AI Workflow Test Automation Framework

An enterprise-style AI Workflow QA Automation Framework designed to validate modern AI/ML workflows through automated testing, regression detection, performance monitoring, schema validation, and workflow orchestration using Apache Airflow.

## Project Overview

Modern AI/ML platforms such as Rubiscape involve multiple interconnected components:

- Data ingestion
- Preprocessing
- Feature engineering
- Model inference
- Prediction validation
- Analytics & reporting

Traditional QA strategies are insufficient for validating such dynamic workflows.

This project implements a modular, reusable, and automated testing framework for validating AI workflows end-to-end.

---

## Key Features

### API Testing
- Automated endpoint validation
- HTTP response validation
- Status code checks
- Functional API testing

### Schema Validation
- JSON schema validation
- Required field checks
- Data type validation
- Range validation
- Invalid output detection

### Regression Testing
- Baseline comparison
- Prediction consistency checks
- Drift/deviation detection
- Invalid output validation

### Performance Monitoring
- API latency tracking
- Threshold validation
- Performance logging

### Logging
- Centralized logging system
- Execution logs
- Regression logs
- Performance logs

### Reporting
- HTML test reports
- Coverage reports
- Timestamped report generation

### Workflow Automation
- Apache Airflow orchestration
- Automated QA pipeline execution
- Sequential workflow execution

### CI/CD
- GitHub Actions integration
- Automated test execution

---

## Project Architecture

```text
Apache Airflow
        ↓
AI Workflow Execution
        ↓
API Testing
        ↓
Schema Validation
        ↓
Regression Testing
        ↓
Performance Testing
        ↓
Coverage + HTML Reports
        ↓
Logs & Results

---

## How to Project

Follow the steps below to replicate and run the project locally.

### 1. Clone Repository

```bash
git clone https://github.com/Arnav-Sonawane/AI-Workflow-Test-Automation.git
cd AI-Workflow-Test-Automation
```

---

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pytest --version
```

---

### 4. Project Setup

Ensure the following folders exist:

```text
reports/
├── html_reports/
├── coverage_reports/

logs/
```

If missing, create them:

#### Windows

```powershell
mkdir reports\html_reports
mkdir reports\coverage_reports
mkdir logs
```

#### Linux / Mac

```bash
mkdir -p reports/html_reports
mkdir -p reports/coverage_reports
mkdir -p logs
```

---

## Running Tests

### Run Complete Test Suite

```bash
pytest
```

---

### Run API Tests

```bash
pytest -m api
```

---

### Run Schema Tests

```bash
pytest -m schema
```

---

### Run Regression Tests

```bash
pytest -m regression
```

---

### Run Performance Tests

```bash
pytest -m performance
```

---

## Generate Reports Manually

Run:

```bash
pytest tests \
--cov=pipeline \
--cov-report=html:reports/coverage_html \
--html=reports/report.html \
--self-contained-html
```

Generated reports:

### HTML Report

```text
reports/html_reports/
```

### Coverage Report

```text
reports/coverage_reports/
```

Open:

```text
report.html
```

or

```text
index.html
```

inside the generated coverage folder.

---

## Running the Pipeline

Run the workflow pipeline:

```bash
python -m pipeline.core
```

---

## Apache Airflow Setup (WSL2 Ubuntu)

This project uses Apache Airflow for workflow orchestration.

### Why WSL2?

Apache Airflow has limited native Windows support.  
The project uses **WSL2 Ubuntu** for stable execution.

---

### Install WSL2

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart system after installation.

---

### Install Ubuntu

Launch Ubuntu and create username/password.

---

### Setup Airflow Environment

Install Python 3.11:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

Create virtual environment:

```bash
mkdir ~/edai-airflow
cd ~/edai-airflow

python3.11 -m venv airflow_linux_env
source airflow_linux_env/bin/activate
```

Install Airflow:

```bash
export AIRFLOW_VERSION=2.10.5
export PYTHON_VERSION=3.11
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

---

### Start Airflow

Set Airflow home:

```bash
export AIRFLOW_HOME=~/edai-airflow/airflow
```

Initialize database:

```bash
airflow db migrate
```

Create admin user:

```bash
airflow users create \
--username admin \
--firstname admin \
--lastname admin \
--role Admin \
--email admin@admin.com \
--password admin
```

---

### Start Scheduler

```bash
airflow scheduler
```

---

### Start Webserver

Open new terminal:

```bash
airflow webserver --port 8080
```

Open dashboard:

```text
http://localhost:8080
```

Login:

```text
Username: admin
Password: admin
```

---

## Airflow DAG Workflow

The Airflow DAG automates:

```text
run_pipeline
      ↓
api_tests
      ↓
schema_tests
      ↓
regression_tests
      ↓
performance_tests
      ↓
generate_reports
```

The DAG file is located at:

```text
airflow/dags/qa_automation_dag.py
```

To enable orchestration, place this file inside your Airflow `dags` folder.

---

## Expected Outputs

After successful execution:

### Reports

- Timestamped HTML test reports
- Coverage reports
- Regression logs
- Performance logs

### Validation

- API correctness
- Schema validation
- Regression consistency
- Performance thresholds
- Workflow execution stability

---

## Troubleshooting

### `pytest: command not found`

Activate virtual environment:

```bash
source venv/bin/activate
```

or

```powershell
venv\Scripts\activate
```

---

### Airflow not working on Windows

Use **WSL2 Ubuntu** instead of native Windows.

---

### DAG not appearing

Restart scheduler and webserver:

```bash
airflow scheduler
airflow webserver --port 8080
```