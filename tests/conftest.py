import pytest
import requests
import os

BASE_URL = "https://jsonplaceholder.typicode.com"

# This checks if the API is reachable at all
# If not, all tests are skipped automatically
@pytest.fixture(autouse=True)
def check_api_available():
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=5)
        if response.status_code != 200:
            pytest.skip("API not reachable — skipping test")
    except requests.exceptions.ConnectionError:
        pytest.skip("No internet connection — skipping test")

# This fixture provides the base URL to any test that needs it
@pytest.fixture
def base_url():
    return BASE_URL

# This fixture provides a sample valid post for tests to use
@pytest.fixture
def sample_post():
    return {
        "userId": 1,
        "title": "Sample Test Post",
        "body": "This is a sample post for testing purposes"
    }

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    htmlpath = config.getoption("--html")
    if htmlpath:
        abs_path = os.path.abspath(htmlpath)
        # file:// URLs are clickable in most modern terminals
        file_url = f"file:///{abs_path.replace(chr(92), '/')}"
        terminalreporter.write_sep("=", "HTML Report Generated", bold=True, green=True)
        terminalreporter.write_line("")
        terminalreporter.write_line("Paste this command to open it:")
        terminalreporter.write_line(f"   Start-Process '{abs_path}'")