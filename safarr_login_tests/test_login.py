import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

WEB_URL = "https://safarr-admin-dev.webelight.co.in/sign-in"

ENTER_EMAIL = "Email is required."
ENTER_PASSWORD = "Password is required."
INVALID_CREDENTIALS = "Invalid credentials Please try again with valid credentials ⚠"
VALID_EMAIL_FORMAT = "Enter a valid email address."


@pytest.fixture(scope="class")
def driver_init(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    request.cls.driver = driver
    request.cls.wait = wait

    yield
    driver.quit()


@pytest.mark.usefixtures("driver_init")
class TestSafarrLogin:

    def refresh_page_and_wait(self):
        self.driver.get(WEB_URL)
        time.sleep(2)

    def email_input_field(self):
        return self.wait.until(EC.presence_of_element_located((By.NAME, "email")))

    def password_input_field(self):
        return self.wait.until(EC.presence_of_element_located((By.NAME, "password")))

    def login_button(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    def email_error(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Email is required.')]")))

    def password_error(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Password is required.')]")))

    def invalid_credentials_error(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Invalid credentials')]")))

    def invalid_format(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='root']//form//div[contains(text(),'Enter a valid email address.')]")))

    def logout_if_logged_in(self):
        try:
            logout_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Logout']")))
            logout_btn.click()
            self.wait.until(EC.url_contains("/sign-in"))
        except Exception:
            pass  # not logged in

    def test_blank_fields(self):
        self.refresh_page_and_wait()
        self.login_button().click()
        time.sleep(1.5)
        assert self.email_error().text == ENTER_EMAIL
        assert self.password_error().text == ENTER_PASSWORD

    def test_invalid_email_valid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys("adm@gmail.com")
        self.password_input_field().send_keys("Admin@123")
        self.login_button().click()
        assert INVALID_CREDENTIALS == self.invalid_credentials_error().text

    def test_valid_email_invalid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys("Admin@gmail.com")
        self.password_input_field().send_keys("adm")
        self.login_button().click()
        assert INVALID_CREDENTIALS == self.invalid_credentials_error().text

    def test_invalid_email_invalid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys("adm@gmail.com")
        self.password_input_field().send_keys("adm")
        self.login_button().click()
        assert INVALID_CREDENTIALS == self.invalid_credentials_error().text

    def test_invalid_email_format(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys("invalidemail")
        self.password_input_field().send_keys("Admin@123")
        self.login_button().click()
        assert self.invalid_format().text == VALID_EMAIL_FORMAT

    def test_valid_email_valid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys("Admin@gmail.com")
        self.password_input_field().send_keys("Admin@123")
        self.login_button().click()

        # Wait for the dashboard to load by URL
        self.wait.until(EC.url_contains("/users"))
        assert "/users" in self.driver.current_url

        self.logout_if_logged_in()