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


class TestCommunityType:

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

    def community(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[contains(text(), 'Communities')]")))

    def community_type(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Community Type']")))

    def search_input(self):
        return self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search by Community Type']")))

    def toggle_for_name(self, name):
        return self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//tbody/tr[1]/td[3]/div[1]/span[1]/label[1]/div[1]")))

    def confirm_button(self):
        return self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[normalize-space()='Confirm']")))

    def cancel_button(self):
        return self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[normalize-space()='Cancel']")))

    def test_valid_email_valid_password(self):
        self.refresh_page_and_wait()
        self.email_input_field().send_keys(config.CORRECT_EMAIL)
        self.password_input_field().send_keys(config.CORRECT_PASSWORD)
        self.login_button().click()
        self.wait.until(EC.url_contains("/users"))
        assert "/users" in self.driver.current_url

    def test_navigate_to_community_type(self):
        # Assume user already logged in from previous test or call login steps here
        self.refresh_page_and_wait()
        # Click on "Communities" menu
        self.community().click()
        time.sleep(1)  # small wait to let submenu appear
        # Click on "Community Type" submenu
        self.community_type().click()
        time.sleep(2)  # wait for Community Type page to load
        # Validate we reached the Community Type page URL or some element unique to that page
        assert "/community-type" in self.driver.current_url

    def test_search(self):
        self.search_input().send_keys(input_field.COMMUNITY_NAME[0])
        time.sleep(2)

    def test_toggle(self):
        self.toggle_for_name(input_field.COMMUNITY_NAME[0]).click()
        time.sleep(1)
        self.confirm_button().click()

        wait = WebDriverWait(self.driver, 10)
        toast = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "notification-title")
        ))
        print("Toast message:", toast.text)
        assert "Community Type has been updated successfully" in toast.text








