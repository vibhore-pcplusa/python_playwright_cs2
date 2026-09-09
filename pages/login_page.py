from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("a:has-text('Login')").first

    def navigate(self):
        self.page.goto("https://staging23.cornerstone2.net/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        # Wait for the network to be idle to ensure login completes and redirects
        self.page.wait_for_load_state("networkidle")
