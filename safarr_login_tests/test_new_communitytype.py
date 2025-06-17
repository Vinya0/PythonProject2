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
import random
import string

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 25)

# Functions

def refresh_page_and_wait():
    driver.get(config.WEB_URL)
    time.sleep(2)

def email_input_field():
    return wait.until(EC.presence_of_element_located((By.NAME, "email")))

def password_input_field():
    return wait.until(EC.presence_of_element_located((By.NAME, "password")))

def login_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

def community():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Communities')]")))

def community_type():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Community Type']")))

def search_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search by Community Type']")))

def toggle_for_name(name):
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[3]/div[1]/span[1]/label[1]/div[1]")))

def confirm_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Confirm']")))

def cancel_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))

def pagination():
    return wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Click Next']")))

def click_edit_icon():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='root']//table/tbody/tr[1]/td[3]//button")))

def open_language_dropdown():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@id, 'react-select-') and contains(@id, '-placeholder')]")))

def select_language_option():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[contains(@id, 'react-select-') and contains(@id, '-option-0')]")))

def language_error():
    return wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(text(), 'Language is required')]")))


def click_submit_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

def click_close_button():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='reset']")))

def edit_community_name():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='reset']")))

def edit_validation_error():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='form-explain']")))

def edit_space_error():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(),'Empty space is not allowed.')]")))

def edit_characters_error():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "div[contains(text(),'Special characters are not allowed.')]")))

def edit_length_error():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "div[contains(text(),'Maximum characters allowed is 30.')]")))

def dropdown():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='select-dropdown-indicator']")))

def dropdown_twentyfive():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='25 / page']")))

def dropdown_fifty():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='50 / page']")))

def dropdown_hundred():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='react-select-59-option-3']")))


# Test Class

class TestCommunityType:

    def test_valid_email_valid_password(self):
        refresh_page_and_wait()
        email_input_field().send_keys(config.CORRECT_EMAIL)
        password_input_field().send_keys(config.CORRECT_PASSWORD)
        login_button().click()
        wait.until(EC.url_contains("/users"))
        assert "/users" in driver.current_url

    def test_navigate_to_community_type(self):
        refresh_page_and_wait()
        community().click()
        time.sleep(1)
        community_type().click()
        time.sleep(2)
        assert "/community-type" in driver.current_url

    def test_pagination_next_button(self):
        for _ in range(5):  # number of times to click
            pagination().click()
            time.sleep(2)

    def test_dropdown(self):
        dropdown().click()  # open dropdown
        dropdown_fifty().click()
        time.sleep(2)

    def test_search(self):
        search_input().send_keys(input_field.COMMUNITY_NAME[0])
        time.sleep(2)


    def test_toggle(self):
        toggle_for_name(input_field.COMMUNITY_NAME[0]).click()
        time.sleep(1)
        confirm_button().click()

        toast = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "notification-title")))
        print("Toast message:", toast.text)
        assert "Community Type has been updated successfully" in toast.text
        time.sleep(1)

    def test_invalid_edit_translation(self):
        click_edit_icon().click()
        click_submit_button().click()
        assert edit_validation_error().text == validation_assert.LANGUAGE
        time.sleep(2)

    def test_edit_translation_close(self):
        click_close_button().click()

    def test_edit_translation(self):
        click_edit_icon().click()
        open_language_dropdown().click()
        select_language_option().click()
        click_submit_button().click()
        time.sleep(2)  # Optional: wait for redirection
        assert "/edit-community-type" in driver.current_url
        time.sleep(2)

        driver.back()
        time.sleep(3)
