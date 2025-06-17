import time
from selenium.webdriver.common.keys import Keys

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
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from safarr_login_tests.test_new_communitytype import cancel_button
import pathlib



chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 25)
clear_input = Keys.CONTROL + "a" + Keys.BACKSPACE
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


def add_community_type():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='ltr:ml-1 rtl:mr-1']")))

def community_name():
        return wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@placeholder='Enter Community Type Name']")))

def community_type_name():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='form-explain' and contains(text(), 'Name is required.')]")))

def generate_random_name(length=8):
    return 'Vinya' + ''.join(random.choices(string.ascii_letters, k=length))


def type_error():
    return wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='form-explain' and text()='Special characters are not allowed.']")))

def edit_space_error():
    return wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='form-explain' and text()='Empty space is not allowed.']")))

def edit_length_error():
    return wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='form-explain' and text()='Maximum characters allowed is 30.']")))

def image_community_type_name():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'border-dashed') and contains(@class, 'cursor-pointer')]")))

def image_upload_input():
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

def image_validation():
    return WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Unsupported')]")))

def save_community_type_name():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Save']")))

def back_community_type_name():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Back']")))

# Test Class

class TestCommunityType:

    def test_valid_email_valid_password(self):
        refresh_page_and_wait()
        email_input_field().send_keys(config.CORRECT_EMAIL)
        password_input_field().send_keys(config.CORRECT_PASSWORD)
        login_button().click()
        # Wait until the "Users" text is visible somewhere on the page
        users_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Users']"))
        )
        assert users_text.is_displayed()

    def test_navigate_to_community_type(self):
        refresh_page_and_wait()
        community().click()
        time.sleep(1)
        community_type().click()
        time.sleep(2)
        Community_Type_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Community Type']"))
        )
        assert Community_Type_text.is_displayed()


    # def test_add_community_type(self):
    #     add_community_type().click()
    #     time.sleep(2)  # Optional: wait for redirection

    # COMMUNITY TYPE NAME
    def test_validate_community_type_name(self):
        add_community_type().click()
        time.sleep(2)
        # community_name().send_keys(clear_input)
        save_community_type_name().click()
        time.sleep(1)
        assert community_type_name().text == validation_assert.EMPTY_COMMUNITY_TYPE_NAME
        time.sleep(1)
        community_name().send_keys("@@@@@@")
        time.sleep(1)
        save_community_type_name().click()
        assert type_error().text == validation_assert.CHARACTERS_COMMUNITY_TYPE_NAME
        community_name().send_keys(clear_input)
        community_name().send_keys("   ")  # Only spaces
        time.sleep(1)
        save_community_type_name().click()
        assert edit_space_error().text == validation_assert.SPACE_COMMUNITY_TYPE_NAME
        time.sleep(2)
        community_name().send_keys(clear_input)
        community_name().send_keys(input_field.MAX_LENGTH[0])
        time.sleep(1)
        save_community_type_name().click()
        assert edit_length_error().text == validation_assert.MAX_LENGTH
    #     time.sleep(2)
    #     community_name().send_keys(clear_input)

    def test_community_type_name(self):
        community_name().send_keys(clear_input)
        random_name = generate_random_name()
        community_name().send_keys(random_name)
        # save_community_type_name().click()
        time.sleep(2)

#IMAGE

    def test_community_invalid_image(self):
        time.sleep(2)

        # Upload unsupported image format
        image_upload_input().send_keys("/home/web-h-044/Downloads/xpath.webm")
        time.sleep(2)

        # Assert validation message
        assert image_validation().text == validation_assert.UNSUPPORTED_FILE

        # Try to close the dialog
        try:
            driver.find_element(By.XPATH, "//button[contains(@class, 'close') or @aria-label='Close']").click()
        except:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        time.sleep(1)
        back_community_type_name().click()
        time.sleep(1)
        add_community_type().click()

    def test_image_remove(self):

        time.sleep(2)

        # Upload unsupported image format
        image_upload_input().send_keys("/home/web-h-044/Downloads/SamplePNGImage_100kbmb.png")
        time.sleep(10)
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button']//*[name()='svg']"))
        )
        close_button.click()
        time.sleep(2)

        back_community_type_name().click()
        time.sleep(1)
        add_community_type().click()

    def test_community_valid_image(self):
        # Enter valid name
        random_name = generate_random_name()
        community_name().send_keys(random_name)

        # Upload valid image
        time.sleep(2)
        image_upload_input().send_keys("/home/web-h-044/Downloads/SamplePNGImage_100kbmb.png")
        time.sleep(5)
        save_community_type_name().click()
    #
    #     # Navigate back
        back_community_type_name().click()
        time.sleep(1)
        add_community_type().click()

    def test_upload_single_image_from_folder(self):
        community_name().clear()
        random_name = generate_random_name()
        community_name().send_keys(random_name)

        # Get one valid image from folder
        folder_path = os.path.abspath(os.path.join(os.getcwd(), "test_assets", "images", "image 1"))
        print(f"Uploading image from: {folder_path}")
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            raise FileNotFoundError("No valid image files found in the folder.")

        image_path = os.path.join(folder_path, image_files[0])
        image_upload_input().send_keys(image_path)
        time.sleep(10)  # Wait for preview

        # Click Save
        save_community_type_name().click()
        time.sleep(2)

        # Close modal (wait for it to disappear)
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'modal-content')]"))
            )
        except:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()


    def test_checkbox(self):
        add_community_type().click()
        community_name().send_keys(clear_input)
        random_name = generate_random_name()
        community_name().send_keys(random_name)
        image_upload_input().send_keys("/home/web-h-044/Downloads/xpath.webm")
        time.sleep(2)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//label[text()='AutoDmPCOYQt']"))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//label[text()='4 sep testing']"))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//label[text()='Brands']"))
        time.sleep(1)
        close_button = driver.find_element(By.XPATH,
                                           "//div[normalize-space()='Brands']//button[contains(@class,'ml-2') and contains(@class,'cursor-pointer')]")
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(2)
        driver.quit()






























