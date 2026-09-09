# Playwright Automation for Cornerstone2 Agencies

This repository contains an automated end-to-end test suite for the Cornerstone2 Agencies functionality, built using Python, Playwright, and Pytest.

## Prerequisites

1. **Python 3.9+** installed on your system.
2. Ensure you have cloned this repository to your local machine.

## Setup Instructions

1. **Create and activate a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   *(On Windows, use `venv\Scripts\activate`)*

2. **Install the required Python dependencies:**
   ```bash
   pip install pytest pytest-playwright
   ```

3. **Install the Playwright browsers:**
   ```bash
   playwright install chromium
   ```
   *(Or just run `playwright install` to install all browsers: Chromium, Firefox, and WebKit)*

## Running the Tests

To run the automated test suite, use the following command from the root directory of the project:

```bash
PYTHONPATH=. pytest tests/
```

### Useful Pytest Flags

- **View the browser while tests run (Headed mode):**
  ```bash
  PYTHONPATH=. pytest tests/ --headed
  ```
- **Run a specific test file:**
  ```bash
  PYTHONPATH=. pytest tests/test_agencies.py
  ```
- **See printed output and live logs in your console:**
  ```bash
  PYTHONPATH=. pytest tests/ -s
  ```

## Project Structure

This project follows the industry-standard **Page Object Model (POM)** design pattern:

- `pages/`: Contains the POM classes that encapsulate the element locators and user actions for specific webpages (e.g., `login_page.py`, `agencies_page.py`). This separates the "how" from the "what".
- `tests/`: Contains the actual Pytest test scripts (e.g., `test_agencies.py`) where the assertions and workflows are defined.
- `pytest.ini`: Configuration file for Pytest. It ensures all test logs are automatically routed into the `app.log` file.
- `app.log`: The output log file where test execution steps and status results are securely recorded.
