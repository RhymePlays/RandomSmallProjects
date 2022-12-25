from selenium import webdriver
from selenium.webdriver.common.by import By
import json


# Vars and Params
udvashLoginRegistrationNumber = "YOUR_REG_NUM_HERE"
udvashLoginPassword = "YOUR_PASS_HERE"
data = []

# Actions
driver = webdriver.Chrome()
driver.get("https://online.udvash-unmesh.com/MasterCourse/Class?masterCourseId=4")

driver.find_element(By.ID, "RegistrationNumber").send_keys(udvashLoginRegistrationNumber)
driver.find_element(By.ID, "btnSubmit").click()
driver.find_element(By.ID, "Password").send_keys(udvashLoginPassword)
driver.find_element(By.CLASS_NAME, "uu-button-style-2").click()

while True:
    try:
        driver.find_element(By.CLASS_NAME, "loadMore").click()
    except:
        break

for item in driver.find_elements(By.CLASS_NAME, "course"):

    data.append({
        "subject": item.find_element(By.CLASS_NAME, "badge").text,
        "chapters": item.find_element(By.CLASS_NAME, "card-title").text,
        "lecture": item.find_element(By.CLASS_NAME, "lectureNo").text,
        "topics": item.find_element(By.CLASS_NAME, "card-body").text,
        "videoPageLink": item.find_element(By.CLASS_NAME, "videoBtn").get_attribute("href"),
        "videoLinkYT": "",
        "pdfNotePageLink": item.find_element(By.CLASS_NAME, "noteBtn").get_attribute("href"),
        "pdfNoteLinkUDV": "",
        # "quizPageLink": item.find_element(By.CLASS_NAME, "noteBtn").get_attribute("href"),
        # "quiz": [{"question": "", "answer": "", "A": "", "B": "", "C":"", "D": ""}],
    })

for index in range(0, len(data)):
    driver.get(data[index]["videoPageLink"])
    data[index]["videoLinkYT"] = driver.find_element(By.ID, "player").get_attribute("src")
    print("YT_Link: "+str(index)+"/"+str(len(data)))

for index in range(0, len(data)):
    driver.get(data[index]["pdfNotePageLink"])
    data[index]["pdfNoteLinkUDV"] = driver.find_element(By.CLASS_NAME, "downloadBtn").get_attribute("href")
    print("pdfNote_Link: "+str(index)+"/"+str(len(data)))

with open("data.json", "w") as f:
    f.write(json.dumps(data))