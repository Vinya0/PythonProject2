# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# import pytest
#
# @pytest.fixture
# def setup():
#     options = Options()
#     options.add_argument("--start-maximized")
#     service = Service("/usr/bin/chromedriver")  # Update if your chromedriver path is different
#     driver = webdriver.Chrome(service=service, options=options)
#     wait = WebDriverWait(driver, 10)  # 10 seconds explicit wait
#     yield driver, wait
#     driver.quit()
