import os
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

url = "https://www.allbirds.com/products/mens-tree-toppers"




def sendText(jsonStrAvailableShoes):

    recipient = os.environ["emailRec"]
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ["senderEmail"]
    password = os.environ["emailPassword"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient

    body = MIMEText(jsonStrAvailableShoes)
    msg.attach(body)

    server = smtplib.SMTP_SSL(smtp_server, port)

    server.login(sender_email, password)
    server.sendmail(sender_email, recipient, msg.as_string())
    server.quit()


driver.get(url)
try:
    closeButton = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[11]/div/div/div[2]/button" )))
    closeButton.click()
except Exception as e:
    print("no close button")
# closeButton = driver.find_element(by=By.XPATH, value="/html/body/div[11]/div/div/div[2]/button")

class Availability:
    def __init__(self):
        self.availableColors = []


available = Availability()

colorsDiv = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]")

colorButtons = colorsDiv.find_elements(by=By.XPATH, value="*")



for button in colorButtons:
    button.click()

    sizeButtonObject = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[1]/div/div/div/div[2]/div/div[3]/ul/li[3]/button")
    
    classNameString = sizeButtonObject.get_attribute('class')

    if "unavailable" not in classNameString:
        colorName = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[2]/div[1]/span[2]").get_attribute('innerHTML')
        available.availableColors.append(colorName)

driver.close()

jsonStrAvailableShoes = json.dumps(available.__dict__)
shoeString = ""
for color in available.availableColors:
    shoeString += color + "\n"

print(shoeString)

saveFile = open("color-list.txt", 'r+')
oldAvailableShoes = saveFile.read()


if jsonStrAvailableShoes != oldAvailableShoes:
    sendText(shoeString)

saveFile.truncate(0)
saveFile.seek(0)
saveFile.write(jsonStrAvailableShoes)
saveFile.close()


