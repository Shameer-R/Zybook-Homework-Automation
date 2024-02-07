from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

# Get regular button elements through the xpath
def getElement(driver, xPath):
    try:
        element = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, xPath))
        )
    finally:
        return element

def login(driver, email, password):

    driver.get("https://www.zybooks.com/")

    loginButton = getElement(driver, "/html/body/div[1]/header/div[2]/div/div/nav/div/ul/li[7]/a/span[2]")
    loginButton.click()

    emailTextBox = getElement(driver, "/html/body/div[2]/div/div/div[1]/div[1]/input")
    emailTextBox.send_keys(email)

    passwordTextBox = getElement(driver, "/html/body/div[2]/div/div/div[1]/div[2]/input")
    passwordTextBox.send_keys(password)

    signInButton = getElement(driver, "/html/body/div[2]/div/div/div[3]/button")
    signInButton.click()



    print("Successfully signed into Zybooks!!!")

def courseSelector(driver):

    try:
        element = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, "/html/body/header/div[1]/div/ul/a/li")
            )
        )
    finally:

        instructorSelected = int(input("\nSelect the number corresponding to your instructor: "))
        index = 0
        instructorList = driver.find_elements(By.CLASS_NAME, "subheading")
        for instructor in instructorList:
            print(instructor.text + " - " + str(index))
            index += 1





def Main():
    email = input("Enter your Zybook email: ")
    password = input("Enter your Zybook password: ")

    driver = webdriver.Firefox()
    login(driver, email, password)
    courseSelector(driver)


Main()