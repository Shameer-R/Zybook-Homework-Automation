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

    print("\nSigning in to zybooks...")

    driver.get("https://www.zybooks.com/")

    loginButton = getElement(driver, "/html/body/div[1]/header/div[2]/div/div/nav/div/ul/li[7]/a/span[2]")
    loginButton.click()

    emailTextBox = getElement(driver, "/html/body/div[2]/div/div/div[1]/div[1]/input")
    emailTextBox.send_keys(email)

    passwordTextBox = getElement(driver, "/html/body/div[2]/div/div/div[1]/div[2]/input")
    passwordTextBox.send_keys(password)

    signInButton = getElement(driver, "/html/body/div[2]/div/div/div[3]/button")
    signInButton.click()

    print("Successfully signed into Zybooks!!!\n")

def courseSelector(driver):

    # Making sure that the course elements are on screen before doing anything.
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
        print("")

        instructorSelected = instructorList[instructorIndex]

        instructorSelected.click()

def getAssignments(driver):
    getAssignmentsButton = getElement(driver, "/html/body/div[2]/div/section[2]/div/div[2]/button[3]")
    getAssignmentsButton.click()

    # Making sure the assignment elements are on screen before doing anything
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

        # Looping through assignments so user can choose what they'd like. Excluding the "Active" and "Past" elements
        for assignment in assignmentList:
            if assignment.text != "Active" and assignment.text != "Past":
                print(str(index) + ": " + assignment.text)
                newAssignments.append(assignment)
                index += 1

        assignmentIndex = int(input("\nSelect the number corresponding to the assignment: "))
        print("")
        assignmentSelection = newAssignments[assignmentIndex]
        assignmentSelection.click()

def completeSlides(driver):
    slides = driver.find_elements(By.CLASS_NAME, "animation-controls")

    for slide in slides:
        # Click the animation start button
        slide.find_element(By.TAG_NAME, "button").click()

        amountOfSlides = slide.find_elements(By.TAG_NAME, "span")

        index = 0

        # Click 2x speed button
        slide.find_element(By.TAG_NAME, "input").click()

        while index < len(amountOfSlides):
            print("Slide: " + str(index + 1) + "/" + str(len(amountOfSlides)) + " completed")
            try:
                playButton = WebDriverWait(driver, 10).until(
                    presence_of_element_located(
                        (By.CSS_SELECTOR, ".play-button")
                    )
                )
            finally:
                playButton.click()
                index += 1
        slide.find_element(By.TAG_NAME, "button").click()
        print("Slide Completed")

def completeMultipleChoice(driver):

    activityInputList = driver.find_elements(By.TAG_NAME, "input")
    if activityInputList:
        for activity in activityInputList:
            activity.click()
        print("Multiple Choice Activity Completed")
    else:
        print("No mutliple choice acttivites on this page")

def completeQuestions(driver):

    # Getting all question containers on the page
    questionElementList = driver.find_elements(By.CLASS_NAME, "question")

    if questionElementList:

        # Looping through question containers

        for questionElement in questionElementList:

            spanElementList = questionElement.find_elements(By.TAG_NAME, "span")

            if len(spanElementList) >= 1:

                checkAnswerButton = spanElementList[0]
                showAnswerButton = spanElementList[1]


                # "Show Answer" button needs to be clicked twice to reveal the answer
                showAnswerButton.click()
                showAnswerButton.click()

                # Get the Parent Question Container
                questionElementParent = questionElement.find_element(By.XPATH, "..")

                # Get the answer
                answerElement = questionElementParent.find_element(By.CLASS_NAME, "forfeit-answer")

                questionElementParent.find_element(By.TAG_NAME, "textarea").send_keys(answerElement.text)

                # Submit Answer

                checkAnswerButton.click()

                print("Question complete")




def completeActivites(driver):
    try:
        activityChecker = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.CLASS_NAME, "activity-type")
            )
        )
    finally:
        activityElements = driver.find_elements(By.CLASS_NAME, "activity-type")
        completeSlides(driver)
        completeMultipleChoice(driver)
        completeQuestions(driver)




def moduleSelector(driver):

    # Going through each page in the specific assignment you chose

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
            print("Page Completed")
        if index == len(moduleElementList):
            break





def Main():
    email = input("Enter your Zybook email: ")
    password = input("Enter your Zybook password: ")

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)


    login(driver, email, password)
    courseSelector(driver)
    getAssignments(driver)
    moduleSelector(driver)


Main()