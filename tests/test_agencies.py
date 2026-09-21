# pyrefly: ignore [missing-import]
import os
import pytest
import logging
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
# pyrefly: ignore [missing-import]
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.agencies_page import AgenciesPage

# Configure basic logging to a file for this test suite
logging.basicConfig(
    filename="app.log", filemode="a", level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def test_agencies_workflow(page: Page):
    """
    Test the complete agency workflow: login, verify agency list, and create a new agency.
    """
    logging.info("Starting test_agencies_workflow")
    
    # Setup Pages
    login_page = LoginPage(page)
    agencies_page = AgenciesPage(page)

    # 1. Log in to staging
    logging.info("Navigating to login page and filling credentials...")
    login_page.navigate()
    login_page.login(os.environ.get("CS_USERNAME"), os.environ.get("CS_PASSWORD"))
    logging.info("Login completed.")

    # 2. Navigate to agencies page
    logging.info("Navigating to agencies URL...")
    response = agencies_page.navigate()
    
    assert response is not None, "Failed to get a response from the target URL."
    assert response.status == 200, f"Target URL returned unexpected status: {response.status}"
    logging.info("Result: ✅ Target URL returned status: 200 (OK)")

    # Read the current grid data
    names = agencies_page.get_all_agency_names()
    assert len(names) > 0, "No agencies found in the grid"
    
    for name in names:
        logging.info(f"Found agency in grid: {name}")

    # 3. Add an agency
    logging.info("Clicking 'Add an Agency' button...")
    agencies_page.click_add_agency()
    
    agency_data = {
        "name": "vj_test_agency",
        "display_name": "VJ_test_agecy_display",
        "address1": "vj_noida_address",
        "address2": "vj_noida_address2",
        "city": "Moradabad",
        "state": "AK",
        "zip": "244001",
        "note": "Autometic Note for the agency"
    }
    
    logging.info(f"Filling out agency form for: {agency_data['name']}")
    agencies_page.fill_and_submit_agency(agency_data)
    
    # 4. Verification
    # The submission completes when the network is idle (handled in POM).
    # Since we are using pytest-playwright, the browser context automatically closes after the test.
    logging.info("Agency creation workflow finished successfully.")

def test_agency_form_empty_submission_validation(page: Page):
    """
    Test that submitting an empty agency form triggers validation
    and prevents creation.
    """
    logging.info("Starting test_agency_form_empty_submission_validation")
    
    # Setup Pages
    login_page = LoginPage(page)
    agencies_page = AgenciesPage(page)

    # 1. Log in to staging
    login_page.navigate()
    login_page.login(os.environ.get("CS_USERNAME"), os.environ.get("CS_PASSWORD"))

    # 2. Navigate to agencies page
    agencies_page.navigate()
    agencies_page.wait_for_grid_to_load()

    # 3. Add an agency
    agencies_page.click_add_agency()

    # 4. Try submitting without filling data
    agencies_page.submit_form_only()

    # 5. Verify validation stops us.
    # If validation works, the page will not navigate away and the form will remain visible.
    expect(agencies_page.agency_name_input).to_be_visible()
    logging.info("Validation correctly stopped the empty form submission.")
