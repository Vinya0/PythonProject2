import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestLogin:
    @pytest.mark.parametrize('user,pwd,should_pass', [
        ("Admin@gmail.com", "Admin123", True),    # Valid credentials
        ("adm@gmail.com", "Admin123", False),     # Invalid username
        ("Admin@gmail.com", "adm", False),        # Invalid password
        ("adm@gmail.com", "adm", False),          # Both invalid
        ("", "", False)                           # Both empty
    ])
    def test_login(self, user, pwd, should_pass):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://safarr-admin-dev.webelight.co.in/sign-in")

        wait = WebDriverWait(driver, 10)

        # Wait for email and password fields
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")

        email_input.clear()
        email_input.send_keys(user)
        password_input.clear()
        password_input.send_keys(pwd)

        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()

        time.sleep(2)  # wait for page response

        if should_pass:
            try:
                # Wait for an element visible after login success
                users_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=root]/div[2]/div/div[2]/div/main/div/div[1]/div/h3")))
                print(f"Login successful for user: {user}")
                assert users_header.is_displayed()
            except Exception as e:
                print("Expected successful login, but Users header not found.")
                print(f"Current URL: {driver.current_url}")
                print(driver.page_source[:500])  # first 500 chars of page source for debugging
                raise e
        else:
            if user == "" and pwd == "":
                # Look for validation errors on empty inputs
                errors = driver.find_elements(By.XPATH, "//span[text()='Required']")
                print(f"Validation errors for empty fields: {[e.text for e in errors]}")
                assert len(errors) >= 2
            else:
                try:
                    # Look for invalid credentials toast message — adjust XPath if needed
                    toast = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//div[contains(text(),'Invalid credentials') or contains(text(),'invalid credentials')]")))
                    print(f"Toast message: {toast.text}")
                    assert "invalid credentials" in toast.text.lower()
                except Exception as ex:
                    print("Expected invalid credentials message not found.")
                    print(f"Current URL: {driver.current_url}")
                    print(driver.page_source[:500])  # snippet for debugging
                    raise ex

        driver.quit()
