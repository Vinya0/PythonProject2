from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time


class CommunityTypePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get("https://safarr-admin-dev.webelight.co.in/community-type")

    def search_input(self):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search by Community Type']")))

    def add_button(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Community Type')]")))

    def click_edit_icon(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//tbody/tr[1]/td[3]/div/span[2]/button")))

    def open_language_dropdown(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'select__control')]")))

    def select_language_option(self, language):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class, 'select__option') and normalize-space(text())='{language}']")))

    def click_submit_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))

    def click_close_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='reset']")))

    def click_translation_button(self):
        # self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']//table")))
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=root]/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[3]/div/span[3]/button/svg/path[1]")))

    def translation_dropdown_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[51]/div/div/div/form/div/div[1]/div/div/div/div/div[2]/div")))

    def translation_language_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.ID, "react-select-15-option-0")))

    def translation_submit_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))

    def translation_close_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='reset']")))

    def pagination(self):
        return self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@aria-label='Click Next']")))


    def select_dropdown_option(self, option_text):
        # Click the dropdown
        dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'select__control')]")))
        dropdown.click()

        # More flexible XPath ignoring spaces (normalize-space)
        option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class, 'select__option') and normalize-space(text())='{option_text}']")))

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

    def wait_for_overlay_to_disappear(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "dialog-overlay")))
        except:
            pass


@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    # Login
    driver.get("https://safarr-admin-dev.webelight.co.in/sign-in")
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("Admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("Admin@123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    wait.until(EC.url_contains("/users"))

    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("setup")
class TestCommunityType:

    def setup_method(self):
        self.page = CommunityTypePage(self.driver)
        self.page.open()

    def test_search_field_displayed(self):
        assert self.page.search_input().is_displayed()

    def test_search_community_type(self):
        search = self.page.search_input()
        search.clear()
        search.send_keys("Vinya")
        time.sleep(2)

    def test_toggle_switch(self):
        # Click the toggle
        self.page.toggle_for_name("Vinya").click()

        # Click Confirm
        self.page.confirm_button().click()

        # Wait for success message
        toast = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Community Type has been updated successfully')]"))
        )

        # Assert it ends with either "Active" or "Inactive"
        assert "Community Type has been updated successfully" in toast.text
        assert toast.text.endswith("Active.") or toast.text.endswith("Inactive.")
        time.sleep(2)
    #
    # def test_pagination_next_button(self):
    #     for _ in range(5):  # number of times to click
    #         self.page.pagination().click()
    #         time.sleep(2)

    # def select_dropdown(self):
    #     dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='select__single-value css-yr46hd-singleValue')]")))
    #     dropdown.click()
    #     time.sleep(2)
    #
    # def test_select_dropdown_option(self):
    #     self.page.select_dropdown_option("50 / page")  # note spaces

    # def test_edit_community_type(self):
    #     self.page.click_edit_icon().click()
    #
    #     # Wait for overlay to disappear fully before proceeding
    #     self.page.wait_for_overlay_to_disappear()
    #     time.sleep(0.5)  # small pause to ensure overlay gone
    #
    #     # Scroll to and click dropdown
    #     dropdown = self.page.open_language_dropdown()
    #     self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    #     dropdown.click()
    #
    #     # Select language option
    #     self.page.select_language_option("English").click()
    #
    #     # Submit the form
    #     self.page.click_submit_button().click()

    def test_translation_flow(self):
        # Click translation icon
        self.page.click_translation_button().click()

        # Click dropdown to open languages
        self.page.translation_dropdown_button().click()

        # Select the language option (English)
        self.page.translation_language_button().click()

        # Submit the translation form
        self.page.translation_submit_button().click()

        # Close the translation dialog
        self.page.translation_close_button().click()








