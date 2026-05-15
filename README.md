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
Render (Cloud FastAPI API)
              ↓
Apache Airflow (WSL2 Ubuntu)
              ↓
Pipeline Execution
              ↓
API Testing
              ↓
Schema Validation
              ↓
Regression Testing
              ↓
Performance Testing
              ↓
Timestamped Reports
```

### Hybrid Architecture

This project follows a hybrid deployment model:

#### Cloud Layer
- FastAPI service deployed on Render
- API endpoints exposed publicly
- Swagger UI for API interaction

#### Local QA Layer
Apache Airflow runs locally using WSL2 Ubuntu and orchestrates:

- Pipeline execution
- API testing
- Schema validation
- Regression testing
- Performance testing
- Report generation

This architecture enables validation of a deployed workflow while keeping deterministic benchmarking local.
```

## Live Deployment

The AI workflow API is deployed on Render.

### API Base URL

https://ai-workflow-api-velc.onrender.com

### Swagger Documentation

https://ai-workflow-api-velc.onrender.com/docs

### Health Check

https://ai-workflow-api-velc.onrender.com/health

### Available Endpoints

#### Health Check

```http
GET /health
```

#### Data Ingestion

```http
POST /api/v1/ingest
```

#### Prediction Endpoint

```http
POST /api/v1/predict
```

The deployed API is validated automatically through Apache Airflow.

## Screenshots

### FastAPI Swagger Documentation
<img width="1851" height="947" alt="image" src="https://github.com/user-attachments/assets/4040bca3-5e3c-4ed2-b433-9a062ae6f38e" />

### Apache Airflow DAG Execution

<img width="1872" height="950" alt="image" src="https://github.com/user-attachments/assets/6322e727-1691-4ccc-b622-603bf2a62688" />

### HTML Test Report

<img width="1854" height="947" alt="image" src="https://github.com/user-attachments/assets/2836f712-a8b3-4d6f-9376-02e75a68494b" />

### Coverage Report

<img width="898" height="392" alt="image" src="https://github.com/user-attachments/assets/8f2e45d2-87f1-415a-a3a0-55765ed4d4ac" />


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

### Run API Tests (Deployed API)

These tests validate the deployed Render API.

```bash
pytest -m api
```

Tests performed:

- Endpoint validation
- Response validation
- Status code checks
- API schema validation

---

### Run Schema Tests

```bash
pytest -m schema
```

Validates:

- Required fields
- Data types
- JSON schema
- Range validation
- Invalid outputs

---

### Run Regression Tests

```bash
pytest -m regression
```

Validates:

- Baseline consistency
- Prediction stability
- Output drift detection

---

### Run Performance Tests

```bash
pytest -m performance
```

Validates:

- Latency thresholds
- Response performance
- Execution timing
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

## Generate Reports

Reports are generated automatically through Airflow or can be generated manually.

### Manual Report Generation

```bash
pytest tests \
--cov=pipeline \
--cov-report=html:reports/coverage_reports \
--html=reports/html_reports/report.html \
--self-contained-html
```

### Generated Outputs

#### HTML Reports

```text
reports/html_reports/
```

Contains timestamped reports:

```text
report_YYYY_MM_DD_HHMMSS.html
```

#### Coverage Reports

```text
reports/coverage_reports/
```

Contains:

```text
index.html
```

for detailed code coverage analysis.
```

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

## Apache Airflow Orchestration

Apache Airflow orchestrates automated quality validation of the deployed AI workflow.

### Airflow Workflow

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

### Workflow Behavior

#### API Tests
Validate the deployed Render API.

#### Schema Tests
Validate deployed API responses against JSON schemas.

#### Regression Tests
Run locally for deterministic baseline comparison.

#### Performance Tests
Run locally to avoid network-related latency distortion.

#### Reports
Generate timestamped HTML and coverage reports automatically.

### DAG File Location

```text
airflow/dags/qa_automation_dag.py
```
```

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

## Tech Stack

### Backend
- FastAPI
- Python

### Testing
- Pytest
- Requests
- JSON Schema
- Pytest HTML
- Pytest Coverage

### Workflow Automation
- Apache Airflow

### Deployment
- Render

### Environment
- WSL2 Ubuntu

### CI/CD
- GitHub Actions
```

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
