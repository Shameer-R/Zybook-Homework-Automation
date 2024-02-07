from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

def getElement(xPath):
    try:
        element = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, xPath))
        )
    finally:
        return element
def login(driver, email, password):

    driver.get("https://www.zybooks.com/")

    loginButton = getElement("/html/body/div[1]/header/div[2]/div/div/nav/div/ul/li[7]/a/span[2]")
    loginButton.click()

    emailTextBox = getElement("/html/body/div[2]/div/div/div[1]/div[1]/input")
    emailTextBox.send_keys(email)

    passwordTextBox = getElement("/html/body/div[2]/div/div/div[1]/div[2]/input")
    passwordTextBox.send_keys(password)

    signInButton = getElement("/html/body/div[2]/div/div/div[3]/button")
    signInButton.click()

    print("Successfully signed into Zybooks!")



email = input("What's your Zybook email?")
password = input("What's your Zybook password?")


with webdriver.Firefox() as driver:

    login(driver, email, password)

