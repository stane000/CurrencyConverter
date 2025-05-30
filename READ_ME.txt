Test Scripts Description
========================

This file describes the purpose and behavior of each batch/script file used for running the currency converter tests.

Instal --------------------------------------------------------------------------------

1. install_my_project.bat
--------------------------
Description:
    This script sets up the development environment from scratch.

Runs:
    - env_create.bat       -> Creates a new virtual environment (.venv)
    - env_packages.bat     -> Installs all required Python packages (e.g., via pip install -r requirements.txt)
    - install_playwright.bat -> Installs Playwright browsers and dependencies

Purpose:
    Ensures the project is fully set up and ready for development or testing.

---


Tests ---------------------------------------------------------------------------------------

run_web_converter_tests.bat
-------------------------------
Description:
    Runs tests that are marked for web-based currency converters (e.g., XE, Wise).

Runs:
    - Activates the virtual environment (.venv\Scripts\activate.bat)
    - Executes: `pytest -s -m web`

Purpose:
    Runs tests that use Playwright 
    

Note:
    Ensure that browsers are installed via Playwright and internet access is available.

---

run_calc_converter_tests.bat *(optional, if exists)*
--------------------------------------------------------
Description:
    Runs tests that use local Windows Calculator for conversion.

Runs:
    - Activates the virtual environment
    - Executes: `pytest -s -m calc`

Purpose:
    Verifies currency conversions using built-in calculator logic or UI automation.

---

run_all_tests.bat
---------------------------------------------
Description:
    Runs all available tests without any marker filtering.

Runs:
    - Activates the virtual environment
    - Executes: `pytest -s`

Purpose:
    For full regression or pre-release testing across all converters.

---

Marker Summary
==============
- web      → tests using `web_xe`, `web_gb`
- calc     → tests using `calc`, `calc2`
- xe_calc  → comparison between `web_xe` and `calc`
- xe_calc2 → comparison between `web_xe` and `calc2`

How to Add New Marked Tests:
----------------------------
- Use `@pytest.mark.<marker_name>` above your test
- Register the marker in `pytest.ini` to avoid warnings

