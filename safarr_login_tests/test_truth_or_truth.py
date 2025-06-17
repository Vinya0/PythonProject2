import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from constant import validation_assert
from safarr_setup.config import config
def get_random_question():
    return f"Test Question {uuid.uuid4()}"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 25)
clear_input = Keys.CONTROL + "a" + Keys.BACKSPACE

#FUNCTION
def refresh_page_and_wait():
    driver.get(config.WEB_URL)
    time.sleep(2)

def email_input_field():
    return wait.until(EC.presence_of_element_located((By.NAME, "email")))

def password_input_field():
    return wait.until(EC.presence_of_element_located((By.NAME, "password")))

def login_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

def games():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Games')]")))

def truth_or_truth():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'flex') and contains(@href, '/truth-or-truth')]")))

def search_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))

def add_question():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='ltr:ml-1 rtl:mr-1']")))

def enter_question():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Question']")))

def save_question():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Save']")))

def close_question():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Close']")))

def question_required():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='form-explain' and text()='Question is required.']")))

def empty_space():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='form-explain' and text()='Empty space is not allowed.']")))

def max_length():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='form-explain' and text()='Maximum characters allowed is 100.']")))

def same_question():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Question Already Exists ⚠')]")))

def new_question():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='notification-title']")))

def active_toggle():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='notification-title']")))

def inactive_toggle():
     return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='notification-title']")))

def toggle():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]/div[1]/span[1]/label[1]/div[1]")))

def confirm_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Confirm']")))

def cancel_button():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))

def edit():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]/div[1]/span[2]/button[1]//*[name()='svg']")))

def edit_language_dropdown():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[text()='Please Select']")))

def language_english():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='English']")))

def language_hindi():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Hindi']")))

def submit():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']")))

def close():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Close']")))

def save():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))

def edit_success_message():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='notification-title']")))

def translation():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]/div[1]/span[3]/button[1]//*[name()='svg']")))

def translation_dropdown():
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[text()='Please Select']")))

def translation_success_message():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='notification-title']")))

def search():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))

#Test cases
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

    def test_navigate_to_truth_or_truth(self):
        refresh_page_and_wait()
        games().click()
        time.sleep(1)
        truth_or_truth().click()
        time.sleep(2)
        Truth_or_Truth_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Truth Or Truth']"))
        )
        assert Truth_or_Truth_text.is_displayed()

    def test_validation(self):
        add_question().click()
        time.sleep(2)
        save_question().click()
        assert question_required().text == validation_assert.QUESTION_REQUIRED
        time.sleep(2)
        close_question().click()

    #     # Test: Empty space only
        add_question().click()
        enter_question().send_keys("    ")  # Send only spaces
        save_question().click()
        assert empty_space().text == validation_assert.EMPTY_SPACE_QUESTION
        time.sleep(2)
        close_question().click()

        # Test: Max length exceeded
        add_question().click()
        long_question = "A" * 101  # 101 characters
        enter_question().send_keys(long_question)
        save_question().click()
        assert max_length().text == validation_assert.QUESTION_MAX_LENGTH
        time.sleep(2)
        close_question().click()

        #Test: Repeated question
        add_question().click()
        enter_question().send_keys("If you had a superpower, what would it be?")
        save_question().click()
        assert same_question().text == validation_assert.EXISTING_QUESTION
        time.sleep(2)
        close_question().click()


    def test_add_question(self):
        add_question().click()
        question = get_random_question()
        enter_question().send_keys(question)
        save_question().click()
        assert new_question().text == validation_assert.NEW_QUESTION
        time.sleep(2)


    def test_toggle(self):
        time.sleep(5)  # wait for any overlay to disappear
        toggle().click()  # click toggle
        time.sleep(1)
        confirm_button().click()  # click confirm
        time.sleep(2)
        assert (active_toggle().text == validation_assert.QUESTION_ACTIVE or
                inactive_toggle().text == validation_assert.QUESTION_INACTIVE)
        time.sleep(2)

    def test_edit(self):
        edit().click()
        edit_language_dropdown().click()
        language_english().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        time.sleep(2)
        save().click()
        assert question_required().text == validation_assert.QUESTION_REQUIRED
        time.sleep(2)
        close().click()

        # Test Empty space only
        edit().click()
        edit_language_dropdown().click()
        language_english().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        enter_question().send_keys("   ")
        time.sleep(2)
        save().click()
        assert empty_space().text == validation_assert.EMPTY_SPACE_QUESTION
        time.sleep(2)
        close().click()

        # Test: Max length
        edit().click()
        edit_language_dropdown().click()
        language_english().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        long_question = "A" * 101  # 101 characters
        enter_question().send_keys(long_question)
        save_question().click()
        assert max_length().text == validation_assert.QUESTION_MAX_LENGTH
        time.sleep(2)
        close_question().click()

        # Test: existing question
        edit().click()
        edit_language_dropdown().click()
        language_english().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        enter_question().send_keys("Test Question 12bc3004-3b5d-400a-8251-f72ca6b9a214")
        time.sleep(2)
        save().click()
        assert same_question().text == validation_assert.EXISTING_QUESTION
        time.sleep(2)
        close().click()

        # Test: Edit success message
        edit().click()
        edit_language_dropdown().click()
        language_english().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        save().click()
        time.sleep(2)
        assert edit_success_message().text == validation_assert.QUESTION_UPDATE
        time.sleep(2)

        # Translation
    def test_translation(self):
        edit().click()
        edit_language_dropdown().click()
        language_english().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        time.sleep(2)
        save().click()
        assert question_required().text == validation_assert.QUESTION_REQUIRED
        time.sleep(2)
        close().click()

        # # Test Empty space only
        translation().click()
        translation_dropdown().click()
        language_hindi().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        enter_question().send_keys("   ")
        time.sleep(2)
        save().click()
        assert empty_space().text == validation_assert.EMPTY_SPACE_QUESTION
        time.sleep(2)
        close().click()

        #  Test: Max length
        translation().click()
        translation_dropdown().click()
        language_hindi().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        long_question = "A" * 101  # 101 characters
        enter_question().send_keys(long_question)
        save_question().click()
        assert max_length().text == validation_assert.QUESTION_MAX_LENGTH
        time.sleep(2)
        close_question().click()

        # Test: Repeated question
        translation().click()
        translation_dropdown().click()
        language_hindi().click()
        time.sleep(2)
        submit().click()
        time.sleep(2)
        enter_question().send_keys(clear_input)
        enter_question().send_keys("national animal")
        time.sleep(2)
        save().click()
        assert same_question().text == validation_assert.EXISTING_QUESTION
        time.sleep(2)
        close().click()

        # Test: Edit success message
        translation().click()
        translation_dropdown().click()
        language_hindi().click()
        time.sleep(2)
        submit().click()
        enter_question().send_keys(clear_input)
        question = get_random_question()
        enter_question().send_keys(question)
        save().click()
        assert translation_success_message().text == validation_assert.GAME_TRANSLATION
        time.sleep(2)

        #search functionality
        search().send_keys("Best place")
        time.sleep(2)
        search().send_keys(clear_input)
        time.sleep(2)
        search().send_keys("Best placeeeee")
        time.sleep(2)





































