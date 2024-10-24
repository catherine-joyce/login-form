from faker import Faker

from selenium import webdriver
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

fake = Faker()
def setup():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    return driver
def test_registration_and_login():
    driver = setup()
    title = driver.title
    assert title == "Register"
    text_box_username = driver.find_element(by=By.ID, value="username")
    fake_username = fake.name()
    text_box_username.send_keys(fake_username)
    text_box_password = driver.find_element(by=By.ID, value="password")
    text_box_password.send_keys("12345678")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    submit_button.click()
    title = driver.title
    assert title == "Login"
    text_box_username = driver.find_element(by=By.ID, value="username")
    text_box_username.send_keys(fake_username)
    text_box_password = driver.find_element(by=By.ID, value="password")
    text_box_password.send_keys("12345678")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    submit_button.click()
    title = driver.title
    assert title == "Login"
    message = driver.find_element(by=By.CSS_SELECTOR, value="p")
    value = message.text
    assert value == f"You are now logged in as {fake_username} Log out"
