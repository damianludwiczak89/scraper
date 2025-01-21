from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
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
driver.get('https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/laptop-asus-vivobook-15x-k3504va-ma480w-15-6-oled-i7-1355u-16gb-ram-1tb-ssd-windows-11-home')
html = driver.page_source
driver.quit
page = BeautifulSoup(html, 'html.parser')
price = page.find('span', class_='whole')
price = int(price.text.replace('\u202f', ''))

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email

if price < 4199:
  message['Subject'] = f'Cena Laptopa spadła! Nowa cena: {price}!'
else:
  message['Subject'] = f'Cena nie spadła. Aktualna cena {price}'

body = "https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/laptop-asus-vivobook-15x-k3504va-ma480w-15-6-oled-i7-1355u-16gb-ram-1tb-ssd-windows-11-home"

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
