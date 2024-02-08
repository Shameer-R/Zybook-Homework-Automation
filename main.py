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


        index = 0
        instructorList = driver.find_elements(By.CLASS_NAME, "subheading")
        for instructor in instructorList:
            print(instructor.text + " - " + str(index))
            index += 1

        instructorIndex = int(input("\nSelect the number corresponding to your instructor: "))

        instructorSelected = instructorList[instructorIndex]

        instructorSelected.click()

def getAssignments(driver):
    getAssignmentsButton = getElement(driver, "/html/body/div[2]/div/section[2]/div/div[2]/button[3]")
    getAssignmentsButton.click()

    try:
        assignmentElement = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/section[2]/div/div[1]/div[3]/h3")
            )
        )
    finally:
        panelList = driver.find_element(By.CLASS_NAME, "panel-content")
        assignmentList = panelList.find_elements(By.TAG_NAME, "h3")

        index = 0

        newAssignments = []

        for assignment in assignmentList:
            if assignment.text != "Active":
                print(str(index) + ": " + assignment.text)
                newAssignments.append(assignment)
                index += 1

        assignmentIndex = int(input("\nSelect the number corresponding to the assignment: "))
        assignmentSelection = newAssignments[assignmentIndex]
        assignmentSelection.click()

def completeMultipleChoice(driver):

    activityInputList = driver.find_elements(By.TAG_NAME, "input")
    if activityInputList:
        for activity in activityInputList:
            activity.click()
        print("Multiple Choice Activity Completed")
    else:
        print("No multiple choice")




def completeActivites(driver):
    try:
        activityChecker = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.CLASS_NAME, "activity-type")
            )
        )
    finally:
        activityElements = driver.find_elements(By.CLASS_NAME, "activity-type")
        completeMultipleChoice(driver)




def moduleSelector(driver):

    index = 0

    while True:
        try:
            moduleElement = WebDriverWait(driver, 10).until(
                presence_of_element_located(
                    (By.CLASS_NAME, "underline")
                )
            )
        finally:
            moduleElementList = driver.find_elements(By.CLASS_NAME, "underline")
            selectedModule = moduleElementList[index]
            selectedModule.click()
            completeActivites(driver)
            driver.execute_script("window.history.go(-1)")
            index += 1
        if index == len(moduleElementList):
            break





def Main():
    email = input("Enter your Zybook email: ")
    password = input("Enter your Zybook password: ")

    driver = webdriver.Firefox()
    login(driver, email, password)
    courseSelector(driver)
    getAssignments(driver)
    moduleSelector(driver)
    driver.quit()


Main()