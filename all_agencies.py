from datetime import time
from time import thread_time_ns
import logging
# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

def test_agencies():
    with sync_playwright() as p:
        # Configure basic logging to a file
        logging.basicConfig(
            filename="app.log", filemode="a", level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info("Application started successfully.")
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()   
        
        # 1. Log in to staging
        login_url = "https://staging23.cornerstone2.net/login"
        print(f"Navigating to {login_url}...")
        logging.info(f"Navigating to login URL: {login_url}")
        page.goto(login_url)
        
        print("Filling in login credentials...")
        logging.info("Filling in login credentials...")
        page.locator("#username").fill("e2e_test_admin")
        page.locator("#password").fill("LcMPITzmtlmS0cPxJqNm")
        
        # Click the Login link. Playwright's wait_for_load_state handles the post-login redirect
        print("Submitting form...")
        logging.info("Submitting form...")
        page.locator("a:has-text('Login')").first.click()
        page.wait_for_load_state("networkidle")
        print("Login completed.")
        logging.info("Login completed.")

        # 2. Navigate to the agencies page to check for 200 OK
        target_url = "https://staging23.cornerstone2.net/agencies?pq=eJxLtDKyqi62MrZScvZ0UbLOtDI0sjSyLrYyNLFS8slPzk5NCcnMTa3Kz0tVAomaWik55qYWZSYn6gdk5KfmZVYoWdcCAKeRFQU%3D"
        print(f"Navigating to target URL: {target_url}")
        logging.info(f"Navigating to target URL: {target_url}")
        response = page.goto(target_url)
        print(page.locator("body > ul > li:nth-child(1) > a > span:nth-child(1)").text_content())
        logging.info(page.locator("body > ul > li:nth-child(1) > a > span:nth-child(1)").text_content())
        #after this span over we have some text we need that before next span start, how to get that text
        print(page.locator("body > ul > li:nth-child(1) > a").text_content())
        logging.info(page.locator("body > ul > li:nth-child(1) > a").text_content())

        # The table loads its data dynamically (via AJAX or Javascript).
        # We must tell Playwright to wait for the first row to appear before we grab .all()
        # otherwise .all() will return an empty list immediately!
        page.locator("#AgencyGridCastleKey > tbody > tr:nth-child(1) > td.sorting_1").wait_for()
        
        agency_cells = page.locator("#AgencyGridCastleKey > tbody > tr > td.sorting_1").all()
        
        for cell in agency_cells:
            print(cell.text_content())
            logging.info(cell.text_content())
        if response:
            if response.status == 200:
                print("Result: ✅ Target URL returned status: 200 (OK)")
                logging.info("Result: ✅ Target URL returned status: 200 (OK)") 
            else:
                print(f"Result: ❌ Target URL returned unexpected status: {response.status}")
                logging.info(f"Result: ❌ Target URL returned unexpected status: {response.status}")
        else:
            print("Result: ❌ Failed to get a response from the target URL.")
            logging.info("Result: ❌ Failed to get a response from the target URL.")
        
        # before browser close it should wait for 2 seconds
        page.wait_for_timeout(2000)
        #Step 2, we will click on add an agency button 
        print(page.locator("#content > a:nth-child(2) > span").text_content())
        logging.info(page.locator("#content > a:nth-child(2) > span").text_content())
        page.locator("#content > a:nth-child(2) > span").click()
        #page.wait_for_load_state("networkidle")
        #after this span we have some text we need that before next span start, how to get that text
        # fill agency name here
        page.locator("#tabs-agency-general > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=text]").fill("vj_test_agency")
        #tabs-agency-general > table > tbody > tr:nth-child(5) > td > input[type=text]
        page.locator("#tabs-agency-general > table > tbody > tr:nth-child(5) > td > input[type=text]").fill("VJ_test_agecy_display")
        #adding address
        page.locator("#Address1").fill("vj_noida_address")
        page.locator("#Address2").fill("vj_noida_address2")
        page.locator("#City").fill("Moradabad")
        #StateId
        #its a drop down above from option text we need to choose "AK"
        page.locator("#StateId").select_option("AK")
        page.locator("#Zip").fill("244001")
        #Note
        #in note text area we have to put the data 
        page.locator(".redactor_box:has(#Note) .redactor_editor").fill("Autometic Note for the agency")

        
        
        #click this button
        #content > div:nth-child(3) > a.btn.btn-success
        page.locator("#content > div:nth-child(3) > a.btn.btn-success").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(7000)
        
        browser.close()

if __name__ == "__main__":
    test_agencies()
