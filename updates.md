```text
Implement the following upgrades and improvements to the existing AI Workflow QA Automation project. The current project structure, pipeline, pytest framework, API tests, regression tests, performance tests, and HTML reporting already exist. Only implement the changes below without rebuilding the existing framework.

==================================================
1. ADD JSON SCHEMA VALIDATION
==================================================

Integrate JSON Schema validation into the API testing framework.

Requirements:
- Use the `jsonschema` Python library.
- Create reusable schema files or schema objects.
- Validate:
  - API response structure
  - Required fields
  - Field data types
  - Nested object structures (if applicable)
- Add both positive and negative validation tests.
- Ensure schema validation failures produce readable pytest error messages.

Example validations:
- missing required fields
- incorrect data types
- invalid structures

Add modular schema validators so they can be reused across future APIs.

==================================================
2. ADD ADVANCED NEGATIVE & EDGE CASE TESTING
==================================================

Expand the framework with enterprise-style edge case testing.

Add tests for:
- malformed JSON
- missing fields
- invalid field types
- empty payloads
- duplicate records
- null values
- invalid score ranges
- invalid API endpoints
- API timeout handling
- slow response handling
- unexpected response formats

Requirements:
- Use pytest parametrization wherever possible.
- Keep tests modular and reusable.
- Add meaningful assertion messages.
- Ensure failures are easy to debug.

==================================================
3. IMPLEMENT CENTRALIZED LOGGING SYSTEM
==================================================

Add structured logging across the framework.

Requirements:
- Use Python logging module.
- Create logs directory automatically.
- Generate:
  - test_execution.log
  - regression.log
  - performance.log
- Log:
  - test start/end
  - failures
  - API response times
  - regression mismatches
  - validation failures
  - performance threshold breaches
- Use proper log formatting with timestamps and log levels.
- Ensure logging works during pytest execution.

==================================================
4. ADD TEST COVERAGE REPORTING
==================================================

Integrate pytest coverage reporting.

Requirements:
- Use pytest-cov.
- Generate:
  - terminal coverage summary
  - HTML coverage report
- Measure:
  - pipeline coverage
  - API test coverage
  - regression test coverage
- Add instructions/commands for running coverage reports.
- Ensure the framework can demonstrate at least 80% workflow coverage.

==================================================
5. CONVERT CURRENT PIPELINE INTO AI WORKFLOW SIMULATION
==================================================

Upgrade the existing student-data pipeline into a more realistic AI workflow simulation.

Current flow:
clean_data -> transform_data -> validate_data

Upgrade into:
data_ingestion -> preprocessing -> feature_transformation -> model_inference -> prediction_validation -> output_generation

Requirements:
- Simulate AI/ML workflow behavior.
- Add a lightweight dummy prediction model.
- Include:
  - prediction confidence
  - invalid prediction handling
  - inference validation
  - output consistency checks
- Keep implementation simple but enterprise-like.
- Maintain compatibility with existing tests wherever possible.
- Add new tests specifically for:
  - model inference
  - prediction validation
  - confidence score validation
  - invalid AI outputs

==================================================
6. ADD CI/CD INTEGRATION
==================================================

Integrate CI/CD automation using GitHub Actions.

Requirements:
- Automatically run tests on:
  - push
  - pull request
- Execute:
  - API tests
  - regression tests
  - performance tests
  - coverage reporting
- Generate test reports automatically.
- Fail pipeline if tests fail.
- Store artifacts:
  - HTML reports
  - coverage reports
- Create a professional GitHub Actions workflow YAML.

==================================================
7. ADD TEST CATEGORIZATION & MARKERS
==================================================

Implement pytest markers/categories.

Required markers:
- api
- regression
- performance
- pipeline
- schema
- aiworkflow

Requirements:
- Configure pytest.ini properly.
- Allow selective execution like:
  pytest -m regression
  pytest -m performance
- Apply markers consistently across all tests.

==================================================
8. ADD CENTRALIZED CONFIGURATION MANAGEMENT
==================================================

Remove hardcoded values from the framework.

Create centralized config management using:
- config.yaml OR settings.json

Move configurable items such as:
- base URLs
- thresholds
- timeout values
- performance limits
- file paths
- report paths

Requirements:
- Load configs dynamically.
- Make framework reusable for future workflows.
- Add proper fallback/default handling.

==================================================
9. IMPROVE REPORTING SYSTEM
==================================================

Enhance reporting beyond current pytest-html output.

Requirements:
- Include:
  - total tests
  - passed/failed/skipped
  - execution duration
  - performance summary
  - regression summary
  - schema validation summary
- Add timestamps and environment information.
- Improve readability and structure of reports.
- Make reports presentation/demo friendly.

==================================================
10. IMPROVE PROJECT STRUCTURE
==================================================

Refactor the project into a clean enterprise-style structure.

Suggested structure:

project/
│
├── tests/
│   ├── api/
│   ├── regression/
│   ├── performance/
│   ├── schema/
│   └── aiworkflow/
│
├── logs/
├── reports/
├── schemas/
├── configs/
├── pipeline/
├── utils/
├── .github/workflows/
│
├── pytest.ini
├── requirements.txt
└── README.md

Requirements:
- Keep imports clean.
- Avoid code duplication.
- Improve modularity and maintainability.

==================================================
11. ADD DOCUMENTATION IMPROVEMENTS
==================================================

Update README and documentation.

Include:
- project overview
- architecture explanation
- workflow diagram explanation
- setup instructions
- execution commands
- coverage generation
- CI/CD explanation
- report generation
- folder structure
- test categories
- future scope

Make documentation professional and enterprise-oriented.

==================================================
12. MAINTAIN BACKWARD COMPATIBILITY
==================================================

Do NOT remove existing working functionality.

Requirements:
- Existing tests should continue to work unless intentionally upgraded.
- Preserve current HTML reporting.
- Preserve current regression logic where applicable.
- Ensure all existing functionality integrates with the upgraded architecture.

==================================================
FINAL GOAL
==================================================

Transform the current pytest-based automation prototype into a modular, enterprise-style AI Workflow QA Automation Framework with:
- AI workflow simulation
- schema validation
- regression detection
- performance monitoring
- centralized configuration
- logging
- CI/CD integration
- coverage reporting
- professional reporting
- scalable architecture
```