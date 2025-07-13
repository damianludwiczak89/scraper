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
receiver_email = "damian_konin@tlen.pl, olga_m922@tlen.pl"
password = os.getenv("EMAIL_PASSWORD")

links = [
   ['https://www.airbnb.pl/rooms/1110043269300501078?photo_id=1859810333&source_impression_id=p3_1752397905_P3ECu5IZ-5iMUATI&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 5416],
   ['https://www.airbnb.pl/rooms/1457230180563789971?photo_id=2242190329&source_impression_id=p3_1752397904_P3QTKep2EaRxFCf5&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 3642],
   ['https://www.airbnb.pl/rooms/31469942?photo_id=2121079081&source_impression_id=p3_1752397905_P3W0oIogPVAADBSM&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4511], 
   ['https://www.airbnb.pl/rooms/14319489?photo_id=192184202&source_impression_id=p3_1752397905_P3qCz4w1RY71gGX-&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4246],
   ['https://www.airbnb.pl/rooms/1137549188556102228?photo_id=1892606846&source_impression_id=p3_1752397905_P3-mGMiggbjyWpJd&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4353],
   ['https://www.airbnb.pl/rooms/4223067?photo_id=119301402&source_impression_id=p3_1752397904_P3zZPwvCSpUbVjjp&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 3361],
   ['https://www.airbnb.pl/rooms/1110043269300501078?photo_id=1859810333&source_impression_id=p3_1752397905_P3ECu5IZ-5iMUATI&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 5416],
   ['https://www.airbnb.pl/rooms/1303533168913125082?photo_id=2088427312&source_impression_id=p3_1752397904_P3HElL7VddIy_mM7&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4468],
   ['']
]

body = ""

for link in links:
    
  driver = webdriver.Chrome(options = chrome_options)
  driver.get(link[0])

  # Sometimes page does not load correctly, added a loop to try few times
  for _ in range(1):
    try:
      WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, '_j1kt73')))
      break
    except TimeoutException:
      pass

  html = driver.page_source
  driver.quit()
  page = BeautifulSoup(html, 'html.parser')
  price = [x.text.strip() for x in page.find_all('span', class_='_j1kt73') if 'zł' in x.text][0]
  print(price)
  price = int(price.replace('\xa0', '').split(',')[0])
  body += f'\n - cena startowa {link[1]}, obecna cena - {price} -- {link[0]} \n\n'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email

message['Subject'] = f'Ceny rzym'



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
