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
def login(driver):

    driver.get("https://www.zybooks.com/")

    loginButton = getElement("/html/body/div[1]/header/div[2]/div/div/nav/div/ul/li[7]/a/span[2]")
    loginButton.click()


with webdriver.Firefox() as driver:

    login(driver)

