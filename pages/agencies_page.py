from playwright.sync_api import Page, expect

class AgenciesPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_agency_btn = page.locator("#content > a:nth-child(2) > span")
        
        # Add Agency Form fields
        self.agency_name_input = page.locator("#tabs-agency-general > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=text]")
        self.display_name_input = page.locator("#tabs-agency-general > table > tbody > tr:nth-child(5) > td > input[type=text]")
        self.address1_input = page.locator("#Address1")
        self.address2_input = page.locator("#Address2")
        self.city_input = page.locator("#City")
        self.state_dropdown = page.locator("#StateId")
        self.zip_input = page.locator("#Zip")
        self.note_editor = page.locator(".redactor_box:has(#Note) .redactor_editor")
        self.submit_btn = page.locator("#content > div:nth-child(3) > a.btn.btn-success")
        
        # Grid elements
        self.agency_grid_first_row = page.locator("#AgencyGridCastleKey > tbody > tr:nth-child(1) > td.sorting_1")
        self.agency_cells = page.locator("#AgencyGridCastleKey > tbody > tr > td.sorting_1")

    def navigate(self):
        url = "https://staging23.cornerstone2.net/agencies?pq=eJxLtDKyqi62MrZScvZ0UbLOtDI0sjSyLrYyNLFS8slPzk5NCcnMTa3Kz0tVAomaWik55qYWZSYn6gdk5KfmZVYoWdcCAKeRFQU%3D"
        response = self.page.goto(url)
        return response

    def wait_for_grid_to_load(self):
        # Using built-in wait_for on the locator ensures it appears before we grab the list
        self.agency_grid_first_row.wait_for()

    def get_all_agency_names(self):
        self.wait_for_grid_to_load()
        return self.agency_cells.all_text_contents()

    def click_add_agency(self):
        self.add_agency_btn.click()

    def submit_form_only(self):
        self.submit_btn.click()

    def fill_and_submit_agency(self, data: dict):
        self.agency_name_input.fill(data["name"])
        self.display_name_input.fill(data["display_name"])
        self.address1_input.fill(data["address1"])
        self.address2_input.fill(data["address2"])
        self.city_input.fill(data["city"])
        self.state_dropdown.select_option(data["state"])
        self.zip_input.fill(data["zip"])
        self.note_editor.fill(data["note"])
        
        self.submit_btn.click()
        # Wait for network idle which indicates form submission finished
        self.page.wait_for_load_state("networkidle")
