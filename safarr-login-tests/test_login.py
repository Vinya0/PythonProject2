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
            dashboard = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Users']")))
            print(f"Login successful for user: {user}")
            assert dashboard.is_displayed()
        elif user == "" and pwd == "":
            errors = driver.find_elements(By.XPATH, "//*[@id=root]/div[2]/div/div[2]/div/div[3]/form/div/div[1]/div/div]")
            print("Validation errors for empty fields:")
            for e in errors:
                print("-", e.text)
            assert len(errors) >= 2
        else:
            toast = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id=1]/div[1]/div[2]')]")))
            print("Toast message on invalid login:", toast.text)
            assert "Invalid credentials Please try again with valid credentials ⚠" in toast.text.lower()

        driver.quit()