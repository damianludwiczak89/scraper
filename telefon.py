from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    "--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    '--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

sender_email = "damian_konin@tlen.pl"
receiver_email = "olmaj92@gmail.com"
password = os.getenv("EMAIL_PASSWORD")

    
driver = webdriver.Chrome(options = chrome_options)
driver.get('https://www.samsung.com/pl/smartphones/galaxy-s25-ultra/buy/')

# Sometimes page does not load correctly, added a loop to try few times
for _ in range(3):
  try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 's-rdo-price')))
    break
  except TimeoutException:
    pass

html = driver.page_source
driver.quit()
page = BeautifulSoup(html, 'html.parser')
prices = page.find_all('span', class_='s-rdo-price')


price = prices[-1].text.split('lub')[-1]
print(price)



body = 'https://www.samsung.com/pl/smartphones/galaxy-s25-ultra/buy/'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email

if int(price[0:5].replace(" ", "")) < 7599:
  message['Subject'] = f'Cena telefonu spadła! Nowa cena: {price}!'
else:
  message['Subject'] = f'cena nie spadła - {price}'

message.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP('poczta.o2.pl', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")