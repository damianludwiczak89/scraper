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
receiver_email = "damian_konin@tlen.pl"
password = os.getenv("EMAIL_PASSWORD")

    
driver = webdriver.Chrome(options = chrome_options)
driver.get('https://www.airbnb.pl/rooms/1110043269300501078?photo_id=1859810333&source_impression_id=p3_1752397905_P3ECu5IZ-5iMUATI&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26')

# Sometimes page does not load correctly, added a loop to try few times
for _ in range(1):
  try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'u1dgw2qm atm_7l_rb934l atm_cs_1peztlj dir dir-ltr')))
    break
  except TimeoutException:
     pass

html = driver.page_source
driver.quit()
page = BeautifulSoup(html, 'html.parser')
price = page.find('span', class_='u1dgw2qm atm_7l_rb934l atm_cs_1peztlj dir dir-ltr')
price = int(price.text.replace('\xa0zł\xa0', ''))

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email

message['Subject'] = f'Cena airbnb {price}!'

body = "'https://www.airbnb.pl/rooms/1110043269300501078?photo_id=1859810333&source_impression_id=p3_1752397905_P3ECu5IZ-5iMUATI&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26"

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
