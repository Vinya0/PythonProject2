import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from safarr_setup.config import config
from constant import validation_assert
from constant import input_field


class TestSafarrLogin:

    def setup_class(self):
        chrome_options = webdriver.ChromeOptions()
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 25)

    def refresh_page_and_wait(self):
        self.driver.get(config.WEB_URL)
        time.sleep(2)

    def email_input_field(self):
        return self.wait.until(EC.presence_of_element_located((By.NAME, "email")))

    def password_input_field(self):
        return self.wait.until(EC.presence_of_element_located((By.NAME, "password")))

    def login_button(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    def email_error(self):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(text(),'{validation_assert.EMPTY_EMAIL_ID}')]")))

    def password_error(self):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(text(),'{validation_assert.EMPTY_PASSWORD}')]")))

    def invalid_credentials_error(self):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(text(),'{validation_assert.INCORRECT_CREDENTIALS}')]")))

    def invalid_format(self):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//*[@id='root']//form//div[contains(text(),'{validation_assert.INVALID_EMAIL}')]")))

    def logout_if_logged_in(self):
        try:
            logout_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Logout']")))
            logout_btn.click()
            self.wait.until(EC.url_contains("/sign-in"))
        except Exception:
            pass  # Not logged in

    def test_blank_fields(self):
        self.refresh_page_and_wait()
        self.login_button().click()
        time.sleep(2)
        assert self.email_error().text == validation_assert.EMPTY_EMAIL_ID
        assert self.password_error().text == validation_assert.EMPTY_PASSWORD

    def test_invalid_email_valid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys(input_field.INVALID_EMAIL[0])
        self.password_input_field().send_keys(config.CORRECT_PASSWORD)
        self.login_button().click()
        assert self.invalid_format().text == validation_assert.INVALID_EMAIL

    def test_valid_email_invalid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys(config.CORRECT_EMAIL)
        self.password_input_field().send_keys(input_field.INCORRECT_PASSWORD)
        self.login_button().click()
        assert self.invalid_credentials_error().text == validation_assert.INCORRECT_CREDENTIALS

    def test_invalid_email_invalid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys(input_field.INVALID_EMAIL[1])
        self.password_input_field().send_keys(input_field.INCORRECT_PASSWORD)
        self.login_button().click()
        assert self.invalid_format().text == validation_assert.INVALID_EMAIL

    def test_invalid_email_format(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys(input_field.INVALID_EMAIL[2])
        self.login_button().click()
        assert self.password_error().text == validation_assert.EMPTY_PASSWORD

    def test_valid_email_valid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys(config.CORRECT_EMAIL)
        self.password_input_field().send_keys(config.CORRECT_PASSWORD)
        self.login_button().click()
        self.wait.until(EC.url_contains("/users"))
        assert "/users" in self.driver.current_url
        self.logout_if_logged_in()
